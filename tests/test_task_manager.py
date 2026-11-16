from core.task_manager import TaskManager, TaskState


def test_create_task() -> None:
    manager = TaskManager()
    task = manager.create_task("Initial task", "Foundation setup")
    assert task.id is not None
    assert task.state == TaskState.QUEUED


def test_state_updates() -> None:
    manager = TaskManager()
    task = manager.create_task("State change")
    manager.set_state(task.id, TaskState.EXECUTING)
    assert manager.get_task(task.id).state == TaskState.EXECUTING
