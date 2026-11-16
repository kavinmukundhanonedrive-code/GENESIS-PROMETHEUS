from __future__ import annotations

from pathlib import Path
from memory.database import MemoryStore


def test_memory_store_round_trip(tmp_path: Path) -> None:
    store = MemoryStore(str(tmp_path / "memory.db"))
    store.upsert_memory("preference", "red-black aesthetic", category="preferences", project="GENESIS")
    assert store.get_memory("preference", "GENESIS") == "red-black aesthetic"


def test_memory_is_project_scoped_and_deletable(tmp_path: Path) -> None:
    store = MemoryStore(str(tmp_path / "memory.db"))
    store.upsert_memory("theme", "red", project="one")
    store.upsert_memory("theme", "blue", project="two")
    assert store.get_memory("theme", "one") == "red"
    assert store.delete_memory("theme", "one")
    assert store.get_memory("theme", "one") is None
    assert store.get_memory("theme", "two") == "blue"
