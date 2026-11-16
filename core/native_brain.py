from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from core.task_manager import TaskManager, TaskState


@dataclass
class BrainStatus:
    name: str
    available: bool = False
    connected: bool = False
    model: str = "unknown"
    latency_ms: Optional[int] = None
    last_error: Optional[str] = None


class NativeBrain:
    def __init__(self, task_manager: TaskManager) -> None:
        self.task_manager = task_manager
        self.brains: Dict[str, BrainStatus] = {
            "native": BrainStatus("Native Brain", True, True, "local-orchestrator"),
            "local": BrainStatus("Local Brain"),
            "gemini": BrainStatus("Gemini Brain"),
            "groq": BrainStatus("Groq Brain"),
        }

    def update_brain_status(
        self,
        brain_name: str,
        available: bool,
        connected: bool,
        model: str = "unknown",
        latency_ms: Optional[int] = None,
        last_error: Optional[str] = None,
    ) -> None:
        if brain_name not in self.brains:
            self.brains[brain_name] = BrainStatus(brain_name)

        brain = self.brains[brain_name]
        brain.available = available
        brain.connected = connected
        brain.model = model
        brain.latency_ms = latency_ms
        brain.last_error = last_error

    def plan(self, title: str, description: str = "") -> str:
        task = self.task_manager.create_task(
            title=title,
            description=description,
            priority=2,
        )
        return task.id

    def delegate(self, task_id: str, brain_name: str) -> dict:
        task = self.task_manager.get_task(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")

        self.task_manager.set_state(task_id, TaskState.DELEGATING)
        return {"task_id": task_id, "brain": brain_name}
