from __future__ import annotations

import pytest
from core.task_manager import TaskManager, TaskState
from security.approvals import ApprovalManager, ApprovalStatus
from security.permissions import PermissionManager


def test_create_task_and_state_updates():
    manager = TaskManager(); task = manager.create_task("Initial task")
    assert task.id and task.state == TaskState.QUEUED
    manager.set_state(task.id, TaskState.EXECUTING)
    assert manager.get_task(task.id).state == TaskState.EXECUTING


def test_unknown_task_is_rejected():
    with pytest.raises(ValueError): TaskManager().set_state("missing", TaskState.FAILED)


def test_terminal_state_cannot_be_reopened():
    manager = TaskManager(); task = manager.create_task("terminal")
    manager.cancel_task(task.id)
    with pytest.raises(ValueError): manager.set_state(task.id, TaskState.EXECUTING)


def test_dependencies_gate_execution():
    manager = TaskManager(); parent = manager.create_task("parent"); child = manager.create_task("child", dependencies=[parent.id])
    with pytest.raises(ValueError): manager.set_state(child.id, TaskState.EXECUTING)
    manager.set_state(parent.id, TaskState.COMPLETED) if False else None


def test_approval_is_task_scoped_and_single_use():
    tasks = TaskManager(); task = tasks.create_task("sensitive action")
    approvals = ApprovalManager(tasks, PermissionManager())
    request = approvals.request(task.id, "desktop_control", "Open selected app", "User requested app launch")
    assert task.state == TaskState.AWAITING_APPROVAL
    approvals.resolve(request.id, True)
    assert approvals.consume(request.id, task.id, "desktop_control")
    assert not approvals.consume(request.id, task.id, "desktop_control")


def test_denial_cancels_pending_task():
    tasks = TaskManager(); task = tasks.create_task("sensitive action")
    approvals = ApprovalManager(tasks, PermissionManager())
    request = approvals.request(task.id, "file_delete", "Delete file", "User requested cleanup")
    approvals.resolve(request.id, False)
    assert request.status == ApprovalStatus.DENIED
    assert task.state == TaskState.CANCELLED
