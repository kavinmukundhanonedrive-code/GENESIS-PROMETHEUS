from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class AppSettings:
    app_name: str = "GENESIS PROMETHEUS"
    app_version: str = "0.1.0"
    db_path: str = str(BASE_DIR / "data" / "prometheus.db")
    log_path: str = str(BASE_DIR / "data" / "logs" / "prometheus.log")
    local_model_endpoint: str = "http://localhost:11434"
    active_local_model: str = "llama3.1"
    gemini_api_key: str = ""
    groq_api_key: str = ""
    startup_minimized: bool = False
    floating_widget_enabled: bool = True
    voice_enabled: bool = False

    def ensure_dirs(self) -> None:
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.log_path).parent.mkdir(parents=True, exist_ok=True)


settings = AppSettings()
settings.ensure_dirs()
