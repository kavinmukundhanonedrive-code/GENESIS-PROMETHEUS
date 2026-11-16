from __future__ import annotations

import requests

from providers.base_provider import ProviderAdapter, ProviderError


class LocalProvider(ProviderAdapter):
    name = "local"

    def __init__(self, endpoint: str = "http://127.0.0.1:11434", model: str = "llama3.1", timeout: float = 45.0) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.timeout = timeout

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=min(self.timeout, 3.0))
            return response.ok
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        try:
            response = requests.get(f"{self.endpoint}/api/tags", timeout=min(self.timeout, 5.0))
            response.raise_for_status()
            return [item["name"] for item in response.json().get("models", []) if item.get("name")]
        except (requests.RequestException, ValueError) as exc:
            raise ProviderError("Could not retrieve Ollama models.") from exc

    def test_connection(self) -> bool:
        return self.is_available()

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.endpoint}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False},
                timeout=self.timeout,
            )
            response.raise_for_status()
            text = response.json().get("response", "").strip()
            if not text:
                raise ProviderError("Ollama returned an empty response.")
            return text
        except requests.RequestException as exc:
            raise ProviderError("Ollama request failed; check that the service and selected model are available.") from exc
        except ValueError as exc:
            raise ProviderError("Ollama returned an invalid response.") from exc
