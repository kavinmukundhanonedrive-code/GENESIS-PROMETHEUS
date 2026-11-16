from __future__ import annotations

from PySide6.QtWidgets import QApplication

from config.provider_preferences import ProviderPreferences
from config.settings import settings
from core.native_brain import NativeBrain
from core.state import SharedState
from core.task_manager import TaskManager
from memory.repository import MemoryRepository
from providers.gemini_provider import GeminiProvider
from providers.groq_provider import GroqProvider
from providers.local_provider import LocalProvider
from security.credentials import CredentialManager
from ui.main_window import MainWindow


def main() -> int:
    app = QApplication([]); app.setApplicationName(settings.app_name); settings.ensure_dirs()
    MemoryRepository(settings.db_path)
    credentials = CredentialManager()
    defaults = {"local": settings.active_local_model, "gemini": settings.gemini_model, "groq": settings.groq_model}
    preferences = ProviderPreferences("data/provider_preferences.json", defaults)
    models = preferences.load()
    providers = {
        "local": LocalProvider(settings.local_model_endpoint, models["local"], settings.request_timeout_seconds),
        "gemini": GeminiProvider(api_key=credentials.get_secret("gemini"), model=models["gemini"], timeout=settings.request_timeout_seconds),
        "groq": GroqProvider(api_key=credentials.get_secret("groq"), model=models["groq"], timeout=settings.request_timeout_seconds),
    }
    tasks, shared = TaskManager(), SharedState(); brain = NativeBrain(tasks, providers)
    window = MainWindow(brain, tasks, shared, providers, credentials, preferences); window.show()
    return app.exec()


if __name__ == "__main__": raise SystemExit(main())
