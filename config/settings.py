from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class AppSettings:
    app_name: str = "GENESIS PROMETHEUS"
    app_version: str = "0.2.0"
    db_path: str = os.getenv("PROMETHEUS_DB_PATH", str(BASE_DIR / "data" / "prometheus.db"))
    local_model_endpoint: str = os.getenv("PROMETHEUS_OLLAMA_URL", "http://127.0.0.1:11434")
    active_local_model: str = os.getenv("PROMETHEUS_OLLAMA_MODEL", "llama3.1")
    gemini_model: str = os.getenv("PROMETHEUS_GEMINI_MODEL", "gemini-2.0-flash")
    groq_model: str = os.getenv("PROMETHEUS_GROQ_MODEL", "llama-3.3-70b-versatile")
    startup_minimized: bool = False
    floating_widget_enabled: bool = True
    request_timeout_seconds: float = 45.0

    def ensure_dirs(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)


settings = AppSettings()
