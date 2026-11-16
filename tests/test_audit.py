from __future__ import annotations

from pathlib import Path

from security.audit import AuditLog


def test_audit_log_records_events(tmp_path: Path) -> None:
    log = AuditLog(tmp_path / "audit.db")
    log.record("task_started", "User started a new analysis task", task_id="abc123", source="native_brain", metadata={"brain": "native"})
    events = log.list_events(10)
    assert len(events) == 1
    assert events[0]["event_type"] == "task_started"
    assert events[0]["task_id"] == "abc123"
