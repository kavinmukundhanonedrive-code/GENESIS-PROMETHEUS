from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = str(db_path)
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL,
                value TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                project TEXT NOT NULL DEFAULT 'global',
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(key, project)
            )""")

    def upsert_memory(self, key: str, value: str, category: str = "general", project: str = "global") -> None:
        with self._connect() as conn:
            conn.execute("""INSERT INTO memories(key,value,category,project) VALUES(?,?,?,?)
                ON CONFLICT(key,project) DO UPDATE SET value=excluded.value, category=excluded.category, updated_at=CURRENT_TIMESTAMP""",
                (key, value, category, project))

    def get_memory(self, key: str, project: str = "global") -> str | None:
        with self._connect() as conn:
            row = conn.execute("SELECT value FROM memories WHERE key=? AND project=?", (key, project)).fetchone()
        return str(row[0]) if row else None

    def search_memories(self, query: str, category: str | None = None, project: str | None = None) -> list[dict[str, Any]]:
        clauses, params = ["(key LIKE ? OR value LIKE ? )"], [f"%{query}%", f"%{query}%"]
        if category:
            clauses.append("category=?"); params.append(category)
        if project:
            clauses.append("project=?"); params.append(project)
        with self._connect() as conn:
            rows = conn.execute("SELECT key,value,category,project,updated_at FROM memories WHERE " + " AND ".join(clauses) + " ORDER BY updated_at DESC LIMIT 100", params).fetchall()
        return [dict(row) for row in rows]

    def delete_memory(self, key: str, project: str = "global") -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM memories WHERE key=? AND project=?", (key, project))
            return cursor.rowcount > 0
