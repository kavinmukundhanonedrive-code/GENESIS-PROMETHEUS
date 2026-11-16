from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Permission:
    name: str
    enabled: bool = False
    require_approval: bool = True


class PermissionManager:
    def __init__(self) -> None:
        self.permissions: Dict[str, Permission] = {
            "desktop_control": Permission("desktop_control", True, True),
            "file_delete": Permission("file_delete", False, True),
            "terminal_execute": Permission("terminal_execute", False, True),
            "network_access": Permission("network_access", True, False),
        }

    def has_permission(self, name: str) -> bool:
        return self.permissions.get(name, Permission(name, False, True)).enabled

    def require_approval(self, name: str) -> bool:
        permission = self.permissions.get(name, Permission(name, False, True))
        return permission.require_approval

    def grant(self, name: str) -> None:
        self.permissions.setdefault(name, Permission(name, False, True))
        self.permissions[name].enabled = True
