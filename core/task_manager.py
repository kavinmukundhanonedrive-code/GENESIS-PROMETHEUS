from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import threading
import time
import uuid
from typing import Any, Dict, List, Optional


class TaskState(str, Enum):
    QUEUED = "queued"
    PLANNING = "planning"
    DELEGATING = "delegating"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


TERMINAL_STATES = {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED}
_ALLOWED_TRANSITIONS = {
    TaskState.QUEUED: {TaskState.PLANNING, TaskState.DELEGATING, TaskState.EXECUTING, TaskState.AWAITING_APPROVAL, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.PLANNING: {TaskState.DELEGATING, TaskState.EXECUTING, TaskState.AWAITING_APPROVAL, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.DELEGATING: {TaskState.EXECUTING, TaskState.VERIFYING, TaskState.AWAITING_APPROVAL, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.EXECUTING: {TaskState.VERIFYING, TaskState.AWAITING_APPROVAL, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.VERIFYING: {TaskState.EXECUTING, TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.AWAITING_APPROVAL: {TaskState.QUEUED, TaskState.EXECUTING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.COMPLETED: set(),
    TaskState.FAILED: set(),
    TaskState.CANCELLED: set(),
}


@dataclass
class Task:
    id: str
    title: str
    description: str = ""
    state: TaskState = TaskState.QUEUED
    priority: int = 1
    parent_task_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    error: Optional[str] = None

    def update_state(self, state: TaskState) -> None:
        self.state = state
        self.updated_at = time.time()


class TaskManager:
    """Thread-safe in-memory task registry with explicit lifecycle transitions."""

    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}
        self._lock = threading.RLock()

    def create_task(self, title: str, description: str = "", priority: int = 1,
                    parent_task_id: Optional[str] = None, dependencies: Optional[List[str]] = None,
                    metadata: Optional[Dict[str, Any]] = None) -> Task:
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        with self._lock:
            deps = list(dependencies or [])
            missing = [dep for dep in deps if dep not in self.tasks]
            if missing:
                raise ValueError(f"Unknown task dependencies: {', '.join(missing)}")
            if parent_task_id and parent_task_id not in self.tasks:
                raise ValueError(f"Unknown parent task: {parent_task_id}")
            task = Task(str(uuid.uuid4()), title.strip(), description, priority=priority,
                        parent_task_id=parent_task_id, dependencies=deps, metadata=dict(metadata or {}))
            self.tasks[task.id] = task
            return task

    def get_task(self, task_id: str) -> Optional[Task]:
        with self._lock:
            return self.tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        with self._lock:
            return sorted(self.tasks.values(), key=lambda task: (-task.priority, task.created_at))

    def set_state(self, task_id: str, state: TaskState) -> None:
        with self._lock:
            task = self.tasks.get(task_id)
            if task is None:
                raise ValueError(f"Task not found: {task_id}")
            if task.state == state:
                return
            if state not in _ALLOWED_TRANSITIONS[task.state]:
                raise ValueError(f"Invalid task transition: {task.state.value} -> {state.value}")
            if state in {TaskState.EXECUTING, TaskState.DELEGATING}:
                blocked = [dep for dep in task.dependencies if self.tasks[dep].state != TaskState.COMPLETED]
                if blocked:
                    raise ValueError(f"Task dependencies are not complete: {', '.join(blocked)}")
            task.update_state(state)

    def fail_task(self, task_id: str, error: str) -> None:
        with self._lock:
            task = self.tasks.get(task_id)
            if task is None:
                raise ValueError(f"Task not found: {task_id}")
            if task.state in TERMINAL_STATES:
                return
            task.error = error
            task.update_state(TaskState.FAILED)

    def cancel_task(self, task_id: str) -> None:
        self.set_state(task_id, TaskState.CANCELLED)

    def complete_task(self, task_id: str) -> None:
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        if task.state != TaskState.VERIFYING:
            self.set_state(task_id, TaskState.VERIFYING)
        self.set_state(task_id, TaskState.COMPLETED)
