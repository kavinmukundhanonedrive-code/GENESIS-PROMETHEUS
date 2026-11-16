from __future__ import annotations

from core.execution_history import ExecutionHistory
from security.action_guard import ActionGuard
from core.task_manager import TaskManager


def test_action_guard_requires_explicit_approval_for_sensitive_task() -> None:
    tasks = TaskManager(); task = tasks.create_task("Delete temp logs")
    guard = ActionGuard(tasks)
    request_id = guard.require_approval(task.id, "file_delete", "Delete old temp files", "Cleanup requested by user")
    assert isinstance(request_id, str)
    assert task.state.value == "awaiting_approval"
    assert guard.resolve(request_id, True) is True
    assert guard.consume(request_id, task.id, "file_delete") is True
