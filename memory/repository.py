from __future__ import annotations

from typing import Any, Dict, List, Optional

from memory.database import MemoryStore


class MemoryRepository:
    def __init__(self, db_path: str) -> None:
        self.store = MemoryStore(db_path)

    def save(self, key: str, value: str, category: str = "general", project: str = "global") -> None:
        self.store.upsert_memory(key, value, category=category, project=project)

    def load(self, key: str) -> Optional[str]:
        return self.store.get_memory(key)

    def find(self, query: str, category: Optional[str] = None, project: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.store.search_memories(query, category=category, project=project)

    def remove(self, key: str) -> None:
        self.store.delete_memory(key)
