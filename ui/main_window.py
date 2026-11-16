from __future__ import annotations

from typing import Optional

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
except ImportError:  # pragma: no cover - UI is optional for headless environments
    QApplication = None
    QMainWindow = object
    QLabel = object
    QVBoxLayout = object
    QWidget = object


class MainWindow(QMainWindow if QApplication is not None else object):
    """Shell for the main Prometheus desktop application."""

    def __init__(self) -> None:
        if QApplication is None:
            raise RuntimeError("PySide6 is required to run the UI shell.")
        super().__init__()
        self.setWindowTitle("GENESIS PROMETHEUS")
        self.resize(1400, 900)

        central = QWidget(self)
        layout = QVBoxLayout(central)
        title = QLabel("OBSERVE. UNDERSTAND. PLAN. EXECUTE. VERIFY.")
        title.setObjectName("titleLabel")
        layout.addWidget(title)
        self.setCentralWidget(central)
