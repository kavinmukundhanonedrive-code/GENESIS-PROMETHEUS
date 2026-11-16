from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SystemSnapshot:
    cpu_percent: float = 0.0
    ram_percent: float = 0.0
    storage_percent: float = 0.0
    active_windows: List[str] = field(default_factory=list)
    active_brain: str = "native"
    provider_status: Dict[str, bool] = field(default_factory=lambda: {"native": True, "local": False, "gemini": False, "groq": False})
    task_id: str = ""


class SharedState:
    def __init__(self) -> None:
        self.current_task_id: str = ""
        self.active_brain: str = "native"
        self.current_task: str = "Idle"
        self.provider_status: Dict[str, bool] = {"native": True, "local": False, "gemini": False, "groq": False}
        self.task_history: List[str] = []
        self.system_snapshot = SystemSnapshot()

    def set_task(self, task_id: str, task_name: str) -> None:
        self.current_task_id = task_id
        self.current_task = task_name
        self.task_history.append(task_name)

    def update_provider(self, provider_name: str, online: bool) -> None:
        self.provider_status[provider_name] = online

    def snapshot(self) -> SystemSnapshot:
        self.system_snapshot.active_brain = self.active_brain
        self.system_snapshot.task_id = self.current_task_id
        self.system_snapshot.provider_status = dict(self.provider_status)
        return self.system_snapshot


shared_state = SharedState()
