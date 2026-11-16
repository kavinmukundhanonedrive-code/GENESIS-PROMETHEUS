from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Permission:
    name: str
    enabled: bool = False
    require_approval: bool = True


class PermissionManager:
    """Default-deny permission registry; automation must request approval."""
    def __init__(self) -> None:
        self.permissions = {
            "desktop_control": Permission("desktop_control", False, True),
            "file_delete": Permission("file_delete", False, True),
            "terminal_execute": Permission("terminal_execute", False, True),
            "network_access": Permission("network_access", True, False),
        }

    def has_permission(self, name: str) -> bool:
        return self.permissions.get(name, Permission(name)).enabled

    def require_approval(self, name: str) -> bool:
        return self.permissions.get(name, Permission(name)).require_approval

    def grant(self, name: str) -> None:
        self.permissions.setdefault(name, Permission(name))
        self.permissions[name].enabled = True

    def revoke(self, name: str) -> None:
        self.permissions.setdefault(name, Permission(name))
        self.permissions[name].enabled = False
