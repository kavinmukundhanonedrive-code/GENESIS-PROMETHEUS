from __future__ import annotations

from core.native_brain import NativeBrain
from core.task_manager import TaskManager


def test_native_brain_plan_and_delegate() -> None:
    manager = TaskManager()
    brain = NativeBrain(manager)
    task_id = brain.plan("Analyse architecture", "Prepare the system model.")
    result = brain.delegate(task_id, "gemini")
    assert result["task_id"] == task_id
    assert result["brain"] == "gemini"
