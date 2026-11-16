from __future__ import annotations

from pathlib import Path

from core.execution_history import ExecutionHistory


def test_execution_history_tracks_task_state(tmp_path: Path) -> None:
    history = ExecutionHistory(tmp_path / "execution.db")
    history.record_result(
        "task-42",
        state="completed",
        summary="The prompt was answered successfully.",
        provider="gemini",
        success=True,
    )
    records = history.get_for_task("task-42")
    assert len(records) == 1
    assert records[0].state == "completed"
    assert records[0].success is True
