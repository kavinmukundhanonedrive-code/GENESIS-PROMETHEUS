from __future__ import annotations

from enum import Enum
from typing import List, Optional


class BrainType(str, Enum):
    NATIVE = "native"
    LOCAL = "local"
    GEMINI = "gemini"
    GROQ = "groq"


class IntelligenceRouter:
    """Select the most appropriate brain(s) for the requested workload."""

    def __init__(self) -> None:
        self._routing_table = {
            "simple": [BrainType.NATIVE],
            "offline": [BrainType.NATIVE, BrainType.LOCAL],
            "document_analysis": [BrainType.NATIVE, BrainType.LOCAL],
            "architecture": [BrainType.NATIVE, BrainType.GEMINI],
            "rapid_classification": [BrainType.NATIVE, BrainType.GROQ],
            "development": [BrainType.NATIVE, BrainType.GEMINI, BrainType.LOCAL, BrainType.GROQ],
            "research": [BrainType.NATIVE, BrainType.GEMINI, BrainType.GROQ],
        }

    def route(self, task_type: str, *, offline_mode: bool = False, prefer_local: bool = False) -> List[str]:
        normalized = task_type.lower().replace("-", "_")

        if offline_mode and normalized in {"architecture", "research", "development"}:
            normalized = "offline"

        if prefer_local and normalized == "simple":
            return [BrainType.NATIVE.value, BrainType.LOCAL.value]

        route = self._routing_table.get(normalized, [BrainType.NATIVE.value])
        return [brain.value if isinstance(brain, BrainType) else str(brain) for brain in route]

    def route_for_prompt(self, prompt: str, *, offline_mode: bool = False) -> List[str]:
        prompt_lower = prompt.lower()
        if "code" in prompt_lower or "debug" in prompt_lower or "fix" in prompt_lower:
            return self.route("development", offline_mode=offline_mode)
        if "research" in prompt_lower or "compare" in prompt_lower or "fact" in prompt_lower:
            return self.route("research", offline_mode=offline_mode)
        if "summarize" in prompt_lower or "classify" in prompt_lower:
            return self.route("rapid_classification", offline_mode=offline_mode)
        if "document" in prompt_lower or "read" in prompt_lower or "pdf" in prompt_lower:
            return self.route("document_analysis", offline_mode=offline_mode)
        if "architecture" in prompt_lower or "system" in prompt_lower:
            return self.route("architecture", offline_mode=offline_mode)
        return self.route("simple", offline_mode=offline_mode)
