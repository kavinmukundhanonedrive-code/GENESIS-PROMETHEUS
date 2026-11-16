from __future__ import annotations

from enum import Enum
from typing import Dict, List


class BrainType(str, Enum):
    NATIVE = "native"
    LOCAL = "local"
    GEMINI = "gemini"
    GROQ = "groq"


class IntelligenceRouter:
    """Rule-based routing; provider outputs never control permissions or routing."""

    ROUTES: Dict[str, List[str]] = {
        "simple": ["native"],
        "offline": ["local"],
        "document_analysis": ["local", "gemini"],
        "architecture": ["gemini", "local", "groq"],
        "rapid_classification": ["groq", "local", "gemini"],
        "development": ["local", "gemini", "groq"],
        "research": ["gemini", "groq", "local"],
    }

    def route(self, task_type: str, *, offline_mode: bool = False, prefer_local: bool = False) -> List[str]:
        kind = task_type.lower().replace("-", "_")
        if offline_mode:
            return ["local"]
        candidates = list(self.ROUTES.get(kind, ["local", "groq", "gemini"]))
        if prefer_local and "local" in candidates:
            candidates.remove("local")
            candidates.insert(0, "local")
        return candidates

    def route_for_prompt(self, prompt: str, *, offline_mode: bool = False) -> List[str]:
        text = prompt.lower()
        if offline_mode:
            return ["local"]
        if any(word in text for word in ("code", "debug", "program", "develop", "fix this")):
            return self.route("development")
        if any(word in text for word in ("research", "compare", "sources", "fact check")):
            return self.route("research")
        if any(word in text for word in ("classify", "quick", "briefly")):
            return self.route("rapid_classification")
        if any(word in text for word in ("document", "pdf", "summarize this file")):
            return self.route("document_analysis")
        if any(word in text for word in ("architecture", "design a system")):
            return self.route("architecture")
        return self.route("simple")
