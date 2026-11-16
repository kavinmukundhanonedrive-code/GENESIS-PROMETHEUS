from __future__ import annotations

import threading
import time
from typing import Dict, Optional

from core.task_manager import TaskManager, TaskState
from security.approvals import ApprovalManager
from security.permissions import PermissionManager


class ActionGuard:
    """Simple permission gate for sensitive operations.

    This layer does not execute shell commands itself; it enforces a consistent
    approval-before-action pattern for automation and other sensitive contexts.
    """

    def __init__(self, tasks: TaskManager, approvals: Optional[ApprovalManager] = None,
                 permissions: Optional[PermissionManager] = None) -> None:
        self.tasks = tasks
        self.permissions = permissions or PermissionManager()
        self.approvals = approvals or ApprovalManager(tasks, self.permissions)
        self._lock = threading.RLock()

    def check(self, task_id: str, permission_name: str) -> bool:
        task = self.tasks.get_task(task_id)
        if task is None:
            raise ValueError(f"Unknown task: {task_id}")
        if not self.permissions.has_permission(permission_name):
            return False
        return True

    def require_approval(self, task_id: str, permission_name: str, action: str, rationale: str) -> str:
        with self._lock:
            if self.check(task_id, permission_name):
                return "approved"
            request = self.approvals.request(task_id, permission_name, action, rationale)
            return request.id

    def consume(self, request_id: str, task_id: str, permission_name: str) -> bool:
        return self.approvals.consume(request_id, task_id, permission_name)

    def resolve(self, request_id: str, approved: bool) -> bool:
        request = self.approvals.resolve(request_id, approved)
        return request.status.value == "approved"

    def mark_execution(self, task_id: str, *, state: TaskState, summary: str = "") -> None:
        self.tasks.set_state(task_id, state)
