from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any, Dict, List


@dataclass
class ProjectWorkspace:
    name: str
    root: str
    created_at: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class WorkspaceManager:
    """Project-scoped workspace registry for Developer Mode.

    This layer prevents traversal outside a chosen project directory and provides a
    minimal read/write API for file-backed project work.
    """

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = Path(base_dir).expanduser().resolve()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.projects_file = self.base_dir / "workspaces.json"
        self._projects: Dict[str, ProjectWorkspace] = {}
        self._load()

    def _load(self) -> None:
        if not self.projects_file.exists():
            return
        try:
            data = json.loads(self.projects_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return
        for key, value in (data or {}).items():
            self._projects[key] = ProjectWorkspace(
                name=value.get("name", key),
                root=value.get("root", str(self.base_dir / key)),
                created_at=value.get("created_at", ""),
                metadata=value.get("metadata", {}),
            )

    def _save(self) -> None:
        payload = {
            name: {
                "name": workspace.name,
                "root": workspace.root,
                "created_at": workspace.created_at,
                "metadata": workspace.metadata,
            }
            for name, workspace in self._projects.items()
        }
        self.projects_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def create_project(self, name: str, root: str | Path, *, metadata: Dict[str, Any] | None = None) -> ProjectWorkspace:
        project_name = name.strip()
        if not project_name:
            raise ValueError("Project name cannot be empty.")
        workspace_root = Path(root).expanduser().resolve()
        workspace_root.mkdir(parents=True, exist_ok=True)
        if workspace_root == self.base_dir:
            raise ValueError("Project root must not equal the workspace registry root.")
        project = ProjectWorkspace(
            name=project_name,
            root=str(workspace_root),
            created_at=__import__("datetime").datetime.utcnow().isoformat(timespec="seconds") + "Z",
            metadata=dict(metadata or {}),
        )
        self._projects[project_name] = project
        self._save()
        return project

    def get_project(self, name: str) -> ProjectWorkspace:
        project = self._projects.get(name)
        if project is None:
            raise ValueError(f"Unknown project: {name}")
        return project

    def ensure_project(self, name: str) -> ProjectWorkspace:
        return self.get_project(name)

    def _project_root(self, name: str) -> Path:
        project = self.get_project(name)
        root = Path(project.root).expanduser().resolve()
        root.mkdir(parents=True, exist_ok=True)
        return root

    def _safe_path(self, project_name: str, relative_or_absolute_path: str | Path) -> Path:
        project_root = self._project_root(project_name)
        candidate = Path(relative_or_absolute_path).expanduser()
        if candidate.is_absolute():
            resolved = candidate.resolve()
        else:
            resolved = (project_root / candidate).resolve()
        try:
            resolved.relative_to(project_root)
        except ValueError as exc:
            raise ValueError(f"Path escapes project root: {relative_or_absolute_path}") from exc
        return resolved

    def list_files(self, project_name: str, directory: str = ".") -> List[str]:
        root = self._project_root(project_name)
        target = self._safe_path(project_name, directory)
        if not target.exists():
            return []
        if not target.is_dir():
            raise ValueError(f"Not a directory: {directory}")
        return [str(path.relative_to(root)).replace('\\', '/') for path in sorted(target.rglob("*")) if path.is_file()]

    def read_file(self, project_name: str, relative_path: str | Path) -> str:
        file_path = self._safe_path(project_name, relative_path)
        if not file_path.exists() or not file_path.is_file():
            raise FileNotFoundError(f"File not found: {relative_path}")
        return file_path.read_text(encoding="utf-8")

    def write_file(self, project_name: str, relative_path: str | Path, content: str) -> Path:
        file_path = self._safe_path(project_name, relative_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        return file_path

    def delete_file(self, project_name: str, relative_path: str | Path) -> bool:
        file_path = self._safe_path(project_name, relative_path)
        if not file_path.exists():
            return False
        file_path.unlink()
        return True

    def list_projects(self) -> List[ProjectWorkspace]:
        return list(self._projects.values())
