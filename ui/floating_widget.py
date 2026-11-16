from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget


class FloatingWidget(QMainWindow):
    """Lightweight companion view sharing the same application state."""
    def __init__(self, shared_state, restore_main) -> None:
        super().__init__(); self.state, self.restore_main = shared_state, restore_main
        self.setWindowTitle("Prometheus Companion"); self.setFixedSize(350, 150)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Tool)
        content = QWidget(); layout = QVBoxLayout(content); self.status = QLabel("◈ PROMETHEUS · READY")
        self.task = QLabel("No active task"); self.command = QLineEdit(); self.command.setPlaceholderText("Command input is available in the main window")
        expand = QPushButton("EXPAND COMMAND CENTER"); expand.clicked.connect(self._restore)
        layout.addWidget(self.status); layout.addWidget(self.task); layout.addWidget(expand); self.setCentralWidget(content)

    def _restore(self) -> None:
        self.hide(); self.restore_main()

    def showEvent(self, event) -> None:
        self.task.setText(self.state.current_task or "No active task")
        super().showEvent(event)
