from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class SystemStats:
    cpu_percent: float
    ram_percent: float
    storage_percent: float
    active_applications: list[str]


class SystemMonitor:
    def __init__(self) -> None:
        self._cache: Optional[SystemStats] = None

    def snapshot(self) -> SystemStats:
        try:
            import psutil
        except ImportError:  # pragma: no cover
            return SystemStats(
                cpu_percent=0.0,
                ram_percent=0.0,
                storage_percent=0.0,
                active_applications=[],
            )

        cpu_percent = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory()
        storage = psutil.disk_usage('/')
        apps = [p.name() for p in psutil.process_iter(attrs=['name'])][:10]

        return SystemStats(
            cpu_percent=float(cpu_percent),
            ram_percent=float(ram.percent),
            storage_percent=float((storage.used / storage.total) * 100),
            active_applications=apps,
        )
