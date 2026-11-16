from __future__ import annotations

import json
from pathlib import Path


class ProviderPreferences:
    """Persists provider model names only; secrets are never written here."""
    def __init__(self, path: str | Path, defaults: dict[str, str]) -> None:
        self.path = Path(path)
        self.defaults = dict(defaults)

    def load(self) -> dict[str, str]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return {key: str(data.get(key, value)) for key, value in self.defaults.items()}
        except (OSError, ValueError, TypeError):
            return dict(self.defaults)

    def save(self, values: dict[str, str]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        safe = {key: str(values.get(key, default)).strip() or default for key, default in self.defaults.items()}
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(json.dumps(safe, indent=2), encoding="utf-8")
        temporary.replace(self.path)
