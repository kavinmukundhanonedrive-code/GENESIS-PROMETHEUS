from __future__ import annotations

import os
from typing import Optional


class VoiceService:
    """Voice shell for wake-word and speech processing."""

    def __init__(self) -> None:
        self._listening = False

    def start_listening(self) -> bool:
        self._listening = True
        return True

    def stop_listening(self) -> bool:
        self._listening = False
        return True

    def speak(self, text: str) -> bool:
        return bool(text)

    def enable_wake_word(self, wake_word: str = "Yo Prometheus.") -> bool:
        return bool(wake_word)
