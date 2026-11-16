from __future__ import annotations

try:
    from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
except ImportError:  # pragma: no cover
    QApplication = None
    QMainWindow = object
    QLabel = object
    QVBoxLayout = object
    QWidget = object


class FloatingWidget(QMainWindow if QApplication is not None else object):
    """Compact companion window used when the application is minimized."""

    def __init__(self) -> None:
        if QApplication is None:
            raise RuntimeError("PySide6 is required to run the floating widget.")
        super().__init__()
        self.setWindowTitle("Prometheus")
        self.resize(360, 140)
        self.setWindowFlags(self.windowFlags() | 0x00800000)

        central = QWidget(self)
        layout = QVBoxLayout(central)
        status = QLabel("Native Brain online")
        status.setObjectName("statusLabel")
        layout.addWidget(status)
        self.setCentralWidget(central)
