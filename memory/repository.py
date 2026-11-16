from __future__ import annotations

from typing import Any
from memory.database import MemoryStore


class MemoryRepository:
    def __init__(self, db_path: str) -> None:
        self.store = MemoryStore(db_path)

    def save(self, key: str, value: str, category: str = "general", project: str = "global") -> None:
        self.store.upsert_memory(key, value, category, project)

    def load(self, key: str, project: str = "global") -> str | None:
        return self.store.get_memory(key, project)

    def find(self, query: str, category: str | None = None, project: str | None = None) -> list[dict[str, Any]]:
        return self.store.search_memories(query, category, project)

    def remove(self, key: str, project: str = "global") -> bool:
        return self.store.delete_memory(key, project)
