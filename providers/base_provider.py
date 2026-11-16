"""Provider interfaces for external intelligence services."""

from abc import ABC, abstractmethod


class ProviderAdapter(ABC):
    name: str = "base"

    @abstractmethod
    def is_available(self) -> bool:
        """Return True when the provider can be used."""

    @abstractmethod
    def test_connection(self) -> bool:
        """Perform a connectivity check."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Generate a response for the supplied prompt."""
