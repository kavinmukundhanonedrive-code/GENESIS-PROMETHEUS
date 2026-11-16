from __future__ import annotations

import os

import requests

from providers.base_provider import ProviderAdapter, ProviderError


class GeminiProvider(ProviderAdapter):
    name = "gemini"
    API_ROOT = "https://generativelanguage.googleapis.com/v1beta/models"

    def __init__(self, api_key: str | None = None, model: str = "gemini-2.0-flash", timeout: float = 45.0) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        return bool(self.api_key)

    def test_connection(self) -> bool:
        if not self.is_available():
            return False
        try:
            response = requests.get(self.API_ROOT, params={"key": self.api_key}, timeout=min(self.timeout, 8.0))
            return response.ok
        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        if not self.is_available():
            raise ProviderError("Gemini is not configured. Set GEMINI_API_KEY in the environment.")
        try:
            response = requests.post(
                f"{self.API_ROOT}/{self.model}:generateContent",
                params={"key": self.api_key},
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=self.timeout,
            )
            if response.status_code == 429:
                raise ProviderError("Gemini rate limit reached. Try again later or choose another brain.")
            response.raise_for_status()
            candidates = response.json().get("candidates", [])
            text = "".join(part.get("text", "") for part in candidates[0].get("content", {}).get("parts", [])) if candidates else ""
            if not text.strip():
                raise ProviderError("Gemini returned no text (the response may have been blocked).")
            return text.strip()
        except requests.RequestException as exc:
            raise ProviderError("Gemini request failed; verify network access, model name, and API configuration.") from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Gemini returned an invalid response.") from exc
