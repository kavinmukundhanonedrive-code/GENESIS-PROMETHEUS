from __future__ import annotations

from pathlib import Path


class LocalProvider:
    def __init__(self, endpoint: str = "http://localhost:11434", model: str = "llama3.1") -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model

    def is_available(self) -> bool:
        try:
            import urllib.request
            with urllib.request.urlopen(self.endpoint, timeout=2) as response:
                return getattr(response, "status", 200) < 500
        except Exception:
            return False

    def test_connection(self) -> bool:
        return self.is_available()

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            raise RuntimeError("Local provider is unavailable.")
        return f"Local brain generated a response for: {prompt[:120]}"
