from __future__ import annotations

from PySide6.QtWidgets import QApplication

from config.settings import settings
from core.native_brain import NativeBrain
from core.state import SharedState
from core.task_manager import TaskManager
from memory.repository import MemoryRepository
from providers.gemini_provider import GeminiProvider
from providers.groq_provider import GroqProvider
from providers.local_provider import LocalProvider
from ui.main_window import MainWindow


def main() -> int:
    app = QApplication([])
    app.setApplicationName(settings.app_name)
    settings.ensure_dirs()
    # Initialize memory early so database/setup errors are reported at startup.
    MemoryRepository(settings.db_path)
    providers = {
        "local": LocalProvider(settings.local_model_endpoint, settings.active_local_model, settings.request_timeout_seconds),
        "gemini": GeminiProvider(model=settings.gemini_model, timeout=settings.request_timeout_seconds),
        "groq": GroqProvider(model=settings.groq_model, timeout=settings.request_timeout_seconds),
    }
    tasks, shared = TaskManager(), SharedState()
    brain = NativeBrain(tasks, providers)
    window = MainWindow(brain, tasks, shared)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
