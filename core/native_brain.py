from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from core.intelligence_router import IntelligenceRouter
from core.task_manager import TaskManager, TaskState
from providers.base_provider import ProviderAdapter, ProviderError


@dataclass
class BrainStatus:
    name: str
    available: bool = False
    connected: bool = False
    model: str = "local-orchestrator"
    last_error: str | None = None


class NativeBrain:
    """Deterministic coordinator with provider fallback and local-only mode."""

    def __init__(self, task_manager: TaskManager, providers: Mapping[str, ProviderAdapter] | None = None, router: IntelligenceRouter | None = None) -> None:
        self.task_manager = task_manager
        self.providers = dict(providers or {})
        self.router = router or IntelligenceRouter()
        self.brains = {
            "native": BrainStatus("Native Brain", True, True),
            "local": BrainStatus("Local Brain", "local" in self.providers, False),
            "gemini": BrainStatus("Gemini Brain", "gemini" in self.providers, False),
            "groq": BrainStatus("Groq Brain", "groq" in self.providers, False),
        }

    def update_brain_status(self, brain_name: str, available: bool, connected: bool, model: str = "unknown", latency_ms: int | None = None, last_error: str | None = None) -> None:
        if brain_name in self.brains:
            status = self.brains[brain_name]
            status.available, status.connected, status.model, status.last_error = available, connected, model, last_error

    def plan(self, title: str, description: str = "") -> str:
        return self.task_manager.create_task(title=title, description=description, priority=2).id

    def delegate(self, task_id: str, brain_name: str) -> dict:
        if self.task_manager.get_task(task_id) is None:
            raise ValueError(f"Task not found: {task_id}")
        if brain_name not in self.brains:
            raise ValueError(f"Unknown brain: {brain_name}")
        self.task_manager.set_state(task_id, TaskState.DELEGATING)
        return {"task_id": task_id, "brain": brain_name}

    def respond(self, task_id: str, prompt: str, *, offline_mode: bool = False) -> tuple[str, str]:
        """Run one provider at a time in deterministic preference order; native-only replies stay explicit."""
        task = self.task_manager.get_task(task_id)
        if task is None:
            raise ValueError(f"Task not found: {task_id}")
        self.task_manager.set_state(task_id, TaskState.PLANNING)
        candidates = self.router.route_for_prompt(prompt, offline_mode=offline_mode)
        self.task_manager.set_state(task_id, TaskState.DELEGATING)
        errors: list[str] = []
        for name in candidates:
            provider = self.providers.get(name)
            if provider is None or not provider.is_available():
                continue
            try:
                self.task_manager.set_state(task_id, TaskState.EXECUTING)
                self.brains[name].connected = True
                answer = provider.generate(prompt)
                self.task_manager.set_state(task_id, TaskState.VERIFYING)
                if not answer.strip():
                    raise ProviderError("Provider returned an empty response.")
                self.task_manager.set_state(task_id, TaskState.COMPLETED)
                return answer, name
            except ProviderError as exc:
                errors.append(f"{name}: {exc}")
                self.brains[name].last_error = str(exc)
                self.brains[name].connected = False
        self.task_manager.set_state(task_id, TaskState.COMPLETED)
        if errors:
            return "No intelligence provider completed the request. " + "; ".join(errors), "native"
        if offline_mode:
            return "Offline mode is enabled, but no local model is available. Start Ollama and configure an installed model. No answer was generated.", "native"
        if candidates == ["native"]:
            return "Native Brain is online. No language model was called for this simple request; connect a provider or choose an analysis task to request model assistance.", "native"
        return "No configured provider is available. Configure Ollama, GEMINI_API_KEY, or GROQ_API_KEY in your environment. No answer was fabricated.", "native"
