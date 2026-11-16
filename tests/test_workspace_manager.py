from __future__ import annotations

from pathlib import Path

from developer.workspace_manager import WorkspaceManager


def test_workspace_creation_and_project_file_access(tmp_path: Path) -> None:
    registry = WorkspaceManager(tmp_path / "workspaces")
    project = registry.create_project("PROMETHEUS_APP", tmp_path / "app_project")
    assert project.name == "PROMETHEUS_APP"
    file_path = registry.write_file("PROMETHEUS_APP", "src/app.py", "print('hello')\n")
    assert file_path.name == "app.py"
    assert registry.read_file("PROMETHEUS_APP", "src/app.py") == "print('hello')\n"
    assert "src/app.py" in registry.list_files("PROMETHEUS_APP")


def test_workspace_refuses_traversal(tmp_path: Path) -> None:
    registry = WorkspaceManager(tmp_path / "workspaces")
    registry.create_project("SAFE", tmp_path / "safe_root")
    try:
        registry.read_file("SAFE", "../outside.txt")
        raise AssertionError("Traversal should have been rejected")
    except ValueError:
        pass
