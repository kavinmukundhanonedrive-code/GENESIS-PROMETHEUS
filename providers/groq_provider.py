from __future__ import annotations

import os


class GroqProvider:
    def __init__(self, api_key: str | None = None, model: str = "llama-3.1-8b-instant") -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model

    def is_available(self) -> bool:
        return bool(self.api_key)

    def test_connection(self) -> bool:
        return self.is_available()

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            raise RuntimeError("Groq API key is not configured.")
        return f"Groq brain generated a response for: {prompt[:120]}"
