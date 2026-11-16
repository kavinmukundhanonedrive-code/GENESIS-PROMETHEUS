from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import time
import uuid


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

    def update_state(self, state: TaskState) -> None:
        self.state = state
        self.updated_at = time.time()


class TaskManager:
    def __init__(self) -> None:
        self.tasks: Dict[str, Task] = {}

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: int = 1,
        parent_task_id: Optional[str] = None,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Task:
        task = Task(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            parent_task_id=parent_task_id,
            dependencies=dependencies or [],
            metadata=metadata or {},
        )
        self.tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def list_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    def set_state(self, task_id: str, state: TaskState) -> None:
        task = self.tasks.get(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        task.update_state(state)

    def cancel_task(self, task_id: str) -> None:
        self.set_state(task_id, TaskState.CANCELLED)

    def complete_task(self, task_id: str) -> None:
        self.set_state(task_id, TaskState.COMPLETED)
