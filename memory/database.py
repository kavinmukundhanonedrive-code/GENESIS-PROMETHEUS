from __future__ import annotations

import sqlite3
from typing import Optional, List, Dict, Any


class MemoryStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    category TEXT DEFAULT 'general',
                    project TEXT DEFAULT 'global'
                )
                """
            )
            conn.commit()

    def upsert_memory(self, key: str, value: str, category: str = "general", project: str = "global") -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO memories(key, value, category, project)
                VALUES(?, ?, ?, ?)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    category = excluded.category,
                    project = excluded.project
                """,
                (key, value, category, project),
            )
            conn.commit()

    def get_memory(self, key: str) -> Optional[str]:
        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT value FROM memories WHERE key = ?",
                (key,),
            ).fetchone()
        return row[0] if row else None

    def search_memories(self, query: str, category: Optional[str] = None, project: Optional[str] = None) -> List[Dict[str, Any]]:
        clauses = ["value LIKE ?"]
        params: List[Any] = [f"%{query}%"]

        if category:
            clauses.append("category = ?")
            params.append(category)
        if project:
            clauses.append("project = ?")
            params.append(project)

        sql = "SELECT key, value, category, project FROM memories WHERE " + " AND ".join(clauses)
        with sqlite3.connect(self.db_path) as conn:
            rows = conn.execute(sql, params).fetchall()

        return [
            {"key": key, "value": value, "category": category_name, "project": project_name}
            for key, value, category_name, project_name in rows
        ]

    def delete_memory(self, key: str) -> None:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM memories WHERE key = ?", (key,))
            conn.commit()
