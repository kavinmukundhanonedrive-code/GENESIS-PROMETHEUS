from __future__ import annotations

import os


class GeminiProvider:
    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-pro") -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    def test_connection(self) -> bool:
        return self.is_available()

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            raise RuntimeError("Gemini API key is not configured.")
        return f"Gemini brain generated a response for: {prompt[:120]}"
