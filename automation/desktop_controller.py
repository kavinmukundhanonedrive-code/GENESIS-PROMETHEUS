from __future__ import annotations

from typing import Any, Dict, List


class DesktopController:
    """High-level automation façade for desktop workflows."""

    def __init__(self) -> None:
        self._windows: List[str] = []

    def launch_app(self, app_name: str) -> bool:
        return True if app_name else False

    def switch_window(self, window_name: str) -> bool:
        self._windows.append(window_name)
        return True

    def capture_screenshot(self, path: str) -> str:
        return path

    def list_windows(self) -> List[str]:
        return list(self._windows)
