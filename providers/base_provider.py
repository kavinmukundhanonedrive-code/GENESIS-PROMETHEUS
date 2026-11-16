from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderResponse:
    provider: str
    model: str
    text: str


class ProviderAdapter(ABC):
    name = "base"

    @abstractmethod
    def is_available(self) -> bool:
        """Return whether the provider is configured and reachable."""

    @abstractmethod
    def test_connection(self) -> bool:
        """Make a bounded connectivity check."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate text or raise ProviderError with a safe diagnostic."""


class ProviderError(RuntimeError):
    """Provider failure with no secret values in its message."""
