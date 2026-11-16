from __future__ import annotations

import os

import requests

from providers.base_provider import ProviderAdapter, ProviderError


class GroqProvider(ProviderAdapter):
    name = "groq"
    API_ROOT = "https://api.groq.com/openai/v1"

    def __init__(self, api_key: str | None = None, model: str = "llama-3.3-70b-versatile", timeout: float = 45.0) -> None:
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        return bool(self.api_key)

    def test_connection(self) -> bool:
        if not self.is_available():
            return False
        try:
            response = requests.get(f"{self.API_ROOT}/models", headers={"Authorization": f"Bearer {self.api_key}"}, timeout=min(self.timeout, 8.0))
            return response.ok
        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            raise ProviderError("Groq is not configured. Set GROQ_API_KEY in the environment.")
        try:
            response = requests.post(
                f"{self.API_ROOT}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0.4},
                timeout=self.timeout,
            )
            if response.status_code == 429:
                raise ProviderError("Groq rate limit reached. Try again later or choose another brain.")
            response.raise_for_status()
            text = response.json()["choices"][0]["message"]["content"]
            if not isinstance(text, str) or not text.strip():
                raise ProviderError("Groq returned an empty response.")
            return text.strip()
        except requests.RequestException as exc:
            raise ProviderError("Groq request failed; verify network access, model name, and API configuration.") from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Groq returned an invalid response.") from exc
