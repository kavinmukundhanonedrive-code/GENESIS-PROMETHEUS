from __future__ import annotations

from core.intelligence_router import IntelligenceRouter
from core.native_brain import NativeBrain
from core.task_manager import TaskManager, TaskState
from providers.base_provider import ProviderAdapter


class FakeProvider(ProviderAdapter):
    name = "groq"
    def is_available(self) -> bool: return True
    def test_connection(self) -> bool: return True
    def generate(self, prompt: str) -> str: return "test answer"


def test_native_brain_plan_and_delegate() -> None:
    manager = TaskManager(); brain = NativeBrain(manager, {"groq": FakeProvider()})
    task_id = brain.plan("Analyse architecture")
    assert brain.delegate(task_id, "groq")["brain"] == "groq"


def test_provider_response_completes_task() -> None:
    manager = TaskManager(); brain = NativeBrain(manager, {"groq": FakeProvider()})
    task = manager.create_task("classify", "classify this")
    answer, provider = brain.respond(task.id, "classify this")
    assert (answer, provider) == ("test answer", "groq")
    assert manager.get_task(task.id).state == TaskState.COMPLETED


def test_offline_route_uses_only_local() -> None:
    assert IntelligenceRouter().route_for_prompt("research this", offline_mode=True) == ["local"]
