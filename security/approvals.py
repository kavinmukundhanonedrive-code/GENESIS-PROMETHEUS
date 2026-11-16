from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import threading
import time
import uuid

from core.task_manager import TaskManager, TaskState
from security.permissions import PermissionManager


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    CONSUMED = "consumed"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:
    id: str
    task_id: str
    permission: str
    action: str
    rationale: str
    status: ApprovalStatus
    created_at: float
    expires_at: float


class ApprovalManager:
    """Explicit, expiring, one-use approval records for sensitive operations."""
    def __init__(self, tasks: TaskManager, permissions: PermissionManager, ttl_seconds: int = 300) -> None:
        self.tasks, self.permissions, self.ttl_seconds = tasks, permissions, ttl_seconds
        self._requests: dict[str, ApprovalRequest] = {}
        self._lock = threading.RLock()

    def request(self, task_id: str, permission: str, action: str, rationale: str) -> ApprovalRequest:
        if self.tasks.get_task(task_id) is None:
            raise ValueError("Approval must reference an existing task.")
        if not action.strip() or not rationale.strip():
            raise ValueError("Approval requires a clear action and rationale.")
        now = time.time()
        req = ApprovalRequest(str(uuid.uuid4()), task_id, permission, action.strip(), rationale.strip(), ApprovalStatus.PENDING, now, now + self.ttl_seconds)
        with self._lock:
            self._requests[req.id] = req
        self.tasks.set_state(task_id, TaskState.AWAITING_APPROVAL)
        return req

    def list_pending(self) -> list[ApprovalRequest]:
        with self._lock:
            self._expire_pending()
            return [r for r in self._requests.values() if r.status == ApprovalStatus.PENDING]

    def resolve(self, request_id: str, approve: bool) -> ApprovalRequest:
        with self._lock:
            req = self._requests.get(request_id)
            if req is None:
                raise ValueError("Approval request not found.")
            self._expire_one(req)
            if req.status != ApprovalStatus.PENDING:
                raise ValueError(f"Approval is already {req.status.value}.")
            req.status = ApprovalStatus.APPROVED if approve else ApprovalStatus.DENIED
        task = self.tasks.get_task(req.task_id)
        if task and task.state == TaskState.AWAITING_APPROVAL:
            self.tasks.set_state(req.task_id, TaskState.QUEUED if approve else TaskState.CANCELLED)
        return req

    def consume(self, request_id: str, task_id: str, permission: str) -> bool:
        """Consume an approval only for its exact task and permission; callers still enforce operation safety."""
        with self._lock:
            req = self._requests.get(request_id)
            if req is None:
                return False
            self._expire_one(req)
            if req.status != ApprovalStatus.APPROVED or req.task_id != task_id or req.permission != permission:
                return False
            req.status = ApprovalStatus.CONSUMED
            return True

    def _expire_pending(self) -> None:
        for req in self._requests.values():
            self._expire_one(req)

    @staticmethod
    def _expire_one(req: ApprovalRequest) -> None:
        if req.status == ApprovalStatus.PENDING and time.time() >= req.expires_at:
            req.status = ApprovalStatus.EXPIRED
