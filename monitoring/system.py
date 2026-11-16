from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SystemStats:
    cpu_percent: float | None
    ram_percent: float | None
    storage_percent: float | None
    active_applications: list[str]


class SystemMonitor:
    def snapshot(self) -> SystemStats:
        try:
            import psutil
        except ImportError:
            return SystemStats(None, None, None, [])
        cpu = psutil.cpu_percent(interval=0.1)
        ram = psutil.virtual_memory().percent
        storage = psutil.disk_usage("C:\\" if __import__("os").name == "nt" else "/").percent
        apps = sorted({p.info.get("name", "") for p in psutil.process_iter(attrs=["name"]) if p.info.get("name")})[:20]
        return SystemStats(float(cpu), float(ram), float(storage), apps)
