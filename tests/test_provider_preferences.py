from __future__ import annotations

from config.provider_preferences import ProviderPreferences


def test_preferences_persist_only_model_values(tmp_path):
    prefs = ProviderPreferences(tmp_path / "prefs.json", {"local": "llama3.1", "gemini": "gemini-default"})
    prefs.save({"local": "qwen2.5", "gemini": "gemini-fast"})
    assert prefs.load() == {"local": "qwen2.5", "gemini": "gemini-fast"}
    assert "key" not in (tmp_path / "prefs.json").read_text()
