from __future__ import annotations

from memory.database import MemoryStore


def test_memory_store_round_trip() -> None:
    store = MemoryStore("/tmp/genesis_prometheus_memory_test.db")
    store.upsert_memory("project_preference", "Use red-black aesthetic", category="preferences", project="GENESIS")
    value = store.get_memory("project_preference")
    assert value == "Use red-black aesthetic"


def test_memory_search() -> None:
    store = MemoryStore("/tmp/genesis_prometheus_memory_search_test.db")
    store.upsert_memory("user_setting", "Voice enabled", category="preferences", project="GENESIS")
    matches = store.search_memories("Voice", category="preferences")
    assert any(item["key"] == "user_setting" for item in matches)
