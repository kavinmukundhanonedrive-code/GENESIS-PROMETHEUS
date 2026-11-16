from __future__ import annotations

import pytest
from core.task_manager import TaskManager, TaskState


def test_create_task() -> None:
    manager = TaskManager(); task = manager.create_task("Initial task")
    assert task.id and task.state == TaskState.QUEUED


def test_state_updates() -> None:
    manager = TaskManager(); task = manager.create_task("State change")
    manager.set_state(task.id, TaskState.EXECUTING)
    assert manager.get_task(task.id).state == TaskState.EXECUTING


def test_unknown_task_is_rejected() -> None:
    with pytest.raises(ValueError):
        TaskManager().set_state("missing", TaskState.FAILED)
