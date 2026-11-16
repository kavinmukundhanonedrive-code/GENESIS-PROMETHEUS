from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


class AuditLog:
    """Append-only local event log for user decisions, automation actions, and task state changes."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = Path(db_path).expanduser().resolve()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    task_id TEXT,
                    source TEXT,
                    message TEXT NOT NULL,
                    metadata TEXT DEFAULT '{}'
                )
                """
            )

    def record(self, event_type: str, message: str, *, task_id: str | None = None, source: str = "system", metadata: Optional[Dict[str, Any]] = None) -> None:
        payload = json.dumps(metadata or {}, ensure_ascii=True)
        timestamp = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO audit_events(timestamp, event_type, task_id, source, message, metadata) VALUES (?, ?, ?, ?, ?, ?)",
                (timestamp, event_type, task_id, source, message, payload),
            )

    def list_events(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT timestamp, event_type, task_id, source, message, metadata FROM audit_events ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]
