from __future__ import annotations

import os
import subprocess
from pathlib import Path


class DesktopController:
    """Conservative desktop helpers. Arbitrary command/script execution is not provided."""

    def launch_app(self, executable_path: str) -> subprocess.Popen:
        path = Path(executable_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError("Choose an existing executable by full path.")
        if os.name == "nt" and path.suffix.lower() not in {".exe", ".com", ".bat", ".cmd"}:
            raise ValueError("Only explicit Windows executable paths can be launched.")
        return subprocess.Popen([str(path)], shell=False, close_fds=True)

    def capture_screenshot(self, path: str) -> str:
        try:
            import pyautogui
        except ImportError as exc:
            raise RuntimeError("Install pyautogui and Pillow to enable screenshot capture.") from exc
        target = Path(path).expanduser().resolve()
        target.parent.mkdir(parents=True, exist_ok=True)
        pyautogui.screenshot().save(target)
        return str(target)

    def list_windows(self) -> list[str]:
        if os.name != "nt":
            return []
        try:
            import pygetwindow
            return [title for title in pygetwindow.getAllTitles() if title.strip()]
        except ImportError as exc:
            raise RuntimeError("Install pygetwindow to enumerate Windows applications.") from exc
