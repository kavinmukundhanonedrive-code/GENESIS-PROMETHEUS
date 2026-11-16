from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ExecutionRecord:
    task_id: str
    state: str
    summary: str = ""
    provider: str = "native"
    success: bool = False
    started_at: float = field(default_factory=time.time)
    finished_at: Optional[float] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutionHistory:
    """Local, append-only execution ledger used to verify completion and audit behavior."""

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
                CREATE TABLE IF NOT EXISTS execution_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    provider TEXT NOT NULL,
                    success INTEGER NOT NULL,
                    started_at REAL NOT NULL,
                    finished_at REAL,
                    error TEXT,
                    metadata TEXT NOT NULL DEFAULT '{}'
                )
                """
            )

    def append(self, record: ExecutionRecord) -> ExecutionRecord:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO execution_history(task_id, state, summary, provider, success, started_at, finished_at, error, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    record.task_id,
                    record.state,
                    record.summary,
                    record.provider,
                    int(record.success),
                    record.started_at,
                    record.finished_at,
                    record.error,
                    str(record.metadata),
                ),
            )
        return record

    def record_result(self, task_id: str, *, state: str, summary: str, provider: str = "native", success: bool = False,
                      started_at: Optional[float] = None, finished_at: Optional[float] = None, error: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> ExecutionRecord:
        record = ExecutionRecord(
            task_id=task_id,
            state=state,
            summary=summary,
            provider=provider,
            success=success,
            started_at=started_at if started_at is not None else time.time(),
            finished_at=finished_at,
            error=error,
            metadata=dict(metadata or {}),
        )
        return self.append(record)

    def get_for_task(self, task_id: str) -> List[ExecutionRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT task_id, state, summary, provider, success, started_at, finished_at, error, metadata
                FROM execution_history WHERE task_id = ? ORDER BY id DESC
                """,
                (task_id,),
            ).fetchall()
        return [
            ExecutionRecord(
                task_id=row["task_id"],
                state=row["state"],
                summary=row["summary"],
                provider=row["provider"],
                success=bool(row["success"]),
                started_at=row["started_at"],
                finished_at=row["finished_at"],
                error=row["error"],
                metadata=dict(eval(row["metadata"], {"__builtins__": {}}, {})) if row["metadata"] else {},
            )
            for row in rows
        ]

    def latest(self, task_id: str) -> Optional[ExecutionRecord]:
        records = self.get_for_task(task_id)
        return records[0] if records else None

    def list_recent(self, limit: int = 50) -> List[ExecutionRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT task_id, state, summary, provider, success, started_at, finished_at, error, metadata FROM execution_history ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [
            ExecutionRecord(
                task_id=row["task_id"],
                state=row["state"],
                summary=row["summary"],
                provider=row["provider"],
                success=bool(row["success"]),
                started_at=row["started_at"],
                finished_at=row["finished_at"],
                error=row["error"],
                metadata=dict(eval(row["metadata"], {"__builtins__": {}}, {})) if row["metadata"] else {},
            )
            for row in rows
        ]
