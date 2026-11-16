from __future__ import annotations

from PySide6.QtCore import QObject, QRunnable, Signal, Slot
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QMessageBox, QPushButton, QSplitter, QTextEdit, QVBoxLayout, QWidget)

from core.native_brain import NativeBrain
from core.state import SharedState
from core.task_manager import TaskManager, TaskState
from ui.floating_widget import FloatingWidget


class _Signals(QObject):
    finished = Signal(str, str, str)
    failed = Signal(str, str)


class _AskTask(QRunnable):
    def __init__(self, brain, manager, task_id, prompt, offline):
        super().__init__(); self.brain, self.manager, self.task_id, self.prompt, self.offline = brain, manager, task_id, prompt, offline
        self.signals = _Signals()
    @Slot()
    def run(self):
        try:
            answer, provider = self.brain.respond(self.task_id, self.prompt, offline_mode=self.offline)
            self.signals.finished.emit(self.task_id, provider, answer)
        except Exception as exc:
            self.manager.fail_task(self.task_id, str(exc))
            self.signals.failed.emit(self.task_id, str(exc))


class MainWindow(QMainWindow):
    def __init__(self, brain: NativeBrain, tasks: TaskManager, state: SharedState,
                 providers=None, credentials=None, preferences=None) -> None:
        super().__init__(); self.brain, self.tasks, self.state = brain, tasks, state
        self.providers, self.credentials, self.preferences = providers or {}, credentials, preferences
        self.setWindowTitle("GENESIS PROMETHEUS"); self.resize(1280, 820); self._floating = None; self._workers = set()
        self._build_ui()

    def _build_ui(self):
        from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSplitter
        from PySide6.QtCore import QThreadPool
        self.thread_pool = QThreadPool.globalInstance()
        root = QWidget(); outer = QVBoxLayout(root); outer.setContentsMargins(26, 22, 26, 20)
        header = QHBoxLayout(); brand = QLabel("◈  GENESIS PROMETHEUS"); brand.setObjectName("brand")
        header.addWidget(brand); header.addStretch()
        self.settings_button = QPushButton("SYSTEMS & SETTINGS"); self.settings_button.clicked.connect(self._open_settings); header.addWidget(self.settings_button)
        self.offline = QPushButton("OFFLINE MODE: OFF"); self.offline.setCheckable(True); self.offline.clicked.connect(self._toggle_offline); header.addWidget(self.offline)
        outer.addLayout(header)
        motto = QLabel("OBSERVE. UNDERSTAND. PLAN. EXECUTE. VERIFY."); motto.setObjectName("motto"); outer.addWidget(motto)
        splitter = QSplitter(); left = QWidget(); left_layout = QVBoxLayout(left); left_layout.addWidget(QLabel("INTELLIGENCE SYSTEMS"))
        self.brain_labels = {}
        for key, title in (("native", "Native Brain"), ("local", "Local / Ollama"), ("gemini", "Gemini"), ("groq", "Groq")):
            card = QFrame(); card.setObjectName("brainCard"); row = QHBoxLayout(card); row.addWidget(QLabel(title)); row.addStretch()
            status = QLabel("READY" if key == "native" else "NOT CHECKED"); status.setObjectName("status"); row.addWidget(status); left_layout.addWidget(card); self.brain_labels[key] = status
        left_layout.addStretch(); splitter.addWidget(left)
        right = QWidget(); right_layout = QVBoxLayout(right); right_layout.addWidget(QLabel("COMMAND CONSOLE"))
        self.transcript = QTextEdit(); self.transcript.setReadOnly(True); self.transcript.setPlaceholderText("Your Prometheus conversation will appear here."); right_layout.addWidget(self.transcript, 1)
        entry = QHBoxLayout(); self.command = QLineEdit(); self.command.setPlaceholderText("Describe what you want Prometheus to do…"); self.command.returnPressed.connect(self._submit); entry.addWidget(self.command, 1)
        self.send = QPushButton("EXECUTE"); self.send.clicked.connect(self._submit); entry.addWidget(self.send); right_layout.addLayout(entry)
        actions = QHBoxLayout(); self.cancel = QPushButton("CANCEL CURRENT TASK"); self.cancel.clicked.connect(self._cancel); self.status_line = QLabel("SYSTEM IDLE")
        actions.addWidget(self.cancel); actions.addStretch(); actions.addWidget(self.status_line); right_layout.addLayout(actions)
        splitter.addWidget(right); splitter.setSizes([320, 900]); outer.addWidget(splitter, 1); self.setCentralWidget(root)
        self.setStyleSheet("QMainWindow{background:#08090c;color:#eee} QWidget{color:#eee;font-family:'Segoe UI';font-size:14px} #brand{font-size:24px;font-weight:700;color:#fff} #motto{color:#ed3845;letter-spacing:3px;margin:12px 0 18px} QFrame#brainCard{background:#111318;border:1px solid #392025;border-radius:8px;padding:8px} QLabel#status{color:#ff5964} QPushButton{background:#a80f20;border:0;border-radius:5px;padding:10px 14px;font-weight:600} QPushButton:checked{background:#54121b} QLineEdit,QTextEdit{background:#111318;border:1px solid #39343a;border-radius:5px;padding:10px} QSplitter::handle{background:#242127}")
        self._refresh_brains()

    def _open_settings(self):
        from ui.settings_dialog import SettingsDialog
        if not (self.providers and self.credentials and self.preferences):
            QMessageBox.information(self, "Settings unavailable", "Provider settings are not initialized."); return
        dialog = SettingsDialog(self.providers, self.credentials, self.preferences, self)
        if dialog.exec(): self._refresh_brains()

    def _toggle_offline(self): self.offline.setText("OFFLINE MODE: ON" if self.offline.isChecked() else "OFFLINE MODE: OFF")

    def _submit(self):
        prompt = self.command.text().strip()
        if not prompt: return
        self.command.clear(); self.transcript.append(f"<b style='color:#ff5964'>YOU</b><br/>{prompt}")
        task = self.tasks.create_task(prompt[:80], prompt); self.state.set_task(task.id, prompt[:80]); self.status_line.setText("PLANNING…"); self.send.setEnabled(False)
        worker = _AskTask(self.brain, self.tasks, task.id, prompt, self.offline.isChecked()); self._workers.add(worker)
        worker.signals.finished.connect(self._finished); worker.signals.failed.connect(self._failed)
        worker.signals.finished.connect(lambda *_args, w=worker: self._workers.discard(w)); worker.signals.failed.connect(lambda *_args, w=worker: self._workers.discard(w))
        self.thread_pool.start(worker)

    def _finished(self, task_id, provider, answer):
        task = self.tasks.get_task(task_id)
        cancelled = task is not None and task.state == TaskState.CANCELLED
        self.state.active_brain = provider
        if self.state.current_task_id == task_id:
            self.state.current_task = "Idle"; self.state.current_task_id = ""
        self.transcript.append(f"<b style='color:#ff5964'>{provider.upper()}</b><br/>{answer}")
        self.status_line.setText(f"TASK {task_id[:8]} · {'CANCELLED' if cancelled else task.state.value.upper()} · {provider.upper()}")
        self.send.setEnabled(True); self._refresh_brains()

    def _failed(self, task_id, message):
        if self.state.current_task_id == task_id: self.state.current_task = "Idle"; self.state.current_task_id = ""
        self.transcript.append(f"<b style='color:#ff5964'>ERROR</b><br/>{message}"); self.status_line.setText("TASK FAILED"); self.send.setEnabled(True)

    def _cancel(self):
        task_id = self.state.current_task_id
        if task_id:
            task = self.tasks.get_task(task_id)
            if task and task.state not in {TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELLED}:
                self.tasks.cancel_task(task_id); self.status_line.setText("CANCELLATION REQUESTED · active network request may finish before stopping")

    def _refresh_brains(self):
        for key, label in self.brain_labels.items():
            status = self.brain.brains[key]
            label.setText("ONLINE" if status.connected or key == "native" else ("CONFIGURED" if status.available else "OFFLINE"))

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() == event.Type.WindowStateChange and self.isMinimized():
            if self._floating is None: self._floating = FloatingWidget(self.state, self._restore_main)
            self._floating.show(); self.hide()

    def _restore_main(self): self.showNormal(); self.raise_(); self.activateWindow()
