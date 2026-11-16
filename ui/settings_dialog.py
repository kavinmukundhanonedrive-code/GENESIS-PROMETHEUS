from __future__ import annotations

from PySide6.QtCore import QObject, QRunnable, Signal, Slot
from PySide6.QtWidgets import (QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget)


class _Signals(QObject):
    done = Signal(str, bool, str)


class _ConnectionCheck(QRunnable):
    def __init__(self, name, provider):
        super().__init__(); self.name, self.provider, self.signals = name, provider, _Signals()
    @Slot()
    def run(self):
        try:
            ok = self.provider.test_connection()
            message = "Connected" if ok else "Connection failed or provider is not configured"
        except Exception as exc:
            ok, message = False, str(exc)
        self.signals.done.emit(self.name, ok, message)


class SettingsDialog(QDialog):
    """Provider settings and non-blocking connectivity checks."""
    def __init__(self, providers, credentials, preferences, parent=None):
        super().__init__(parent)
        self.providers, self.credentials, self.preferences = providers, credentials, preferences
        self.setWindowTitle("Prometheus · Systems & Settings"); self.setMinimumWidth(560)
        self._workers = set(); self._model_edits = {}
        outer = QVBoxLayout(self); tabs = QTabWidget(); outer.addWidget(tabs)
        provider_page = QWidget(); form = QFormLayout(provider_page)
        self._key_edits = {}
        labels = {"local": "Ollama", "gemini": "Gemini", "groq": "Groq"}
        for name, provider in providers.items():
            row = QWidget(); row_layout = QHBoxLayout(row); row_layout.setContentsMargins(0, 0, 0, 0)
            model = QLineEdit(provider.model); self._model_edits[name] = model
            row_layout.addWidget(model, 1)
            if name in {"gemini", "groq"}:
                key = QLineEdit(); key.setEchoMode(QLineEdit.Password); key.setPlaceholderText("Leave blank to keep saved key")
                self._key_edits[name] = key
            else:
                key = QLabel(provider.endpoint)
            test = QPushButton("TEST"); test.clicked.connect(lambda checked=False, n=name: self._test(n))
            status = QLabel("Not tested"); status.setMinimumWidth(150); self._status_labels[name] = status if hasattr(self, "_status_labels") else status
            row_layout.addWidget(test); row_layout.addWidget(status)
            form.addRow(labels.get(name, name.title()), row)
            if name in self._key_edits:
                form.addRow(f"{labels[name]} API key", self._key_edits[name])
        tabs.addTab(provider_page, "Intelligence")
        security_page = QWidget(); sec_layout = QVBoxLayout(security_page)
        sec_layout.addWidget(QLabel("Sensitive desktop, terminal, and file-delete permissions are disabled by default. Approval records are task-scoped, expire, and can be consumed only once."))
        tabs.addTab(security_page, "Security")
        buttons = QHBoxLayout(); buttons.addStretch(); save = QPushButton("SAVE SETTINGS"); save.clicked.connect(self._save); close = QPushButton("CLOSE"); close.clicked.connect(self.reject)
        buttons.addWidget(save); buttons.addWidget(close); outer.addLayout(buttons)
        self.setStyleSheet("QDialog{background:#0b0c10;color:#eee} QWidget{color:#eee;font-family:'Segoe UI'} QLineEdit{background:#15161b;border:1px solid #444;padding:8px} QPushButton{background:#a80f20;color:white;border:0;padding:8px 12px;border-radius:4px} QTabWidget::pane{border:1px solid #333}")

    def _test(self, name):
        from PySide6.QtCore import QThreadPool
        worker = _ConnectionCheck(name, self.providers[name]); self._workers.add(worker)
        worker.signals.done.connect(self._test_done); worker.signals.done.connect(lambda *_args, w=worker: self._workers.discard(w))
        self._status_labels[name].setText("Checking…"); QThreadPool.globalInstance().start(worker)

    def _test_done(self, name, ok, message):
        self._status_labels[name].setText(("ONLINE · " if ok else "OFFLINE · ") + message[:90])

    def _save(self):
        try:
            values = {}
            for name, edit in self._model_edits.items():
                model = edit.text().strip()
                if not model: raise ValueError(f"{name} model cannot be empty")
                self.providers[name].model = model; values[name] = model
            for name, edit in self._key_edits.items():
                value = edit.text().strip()
                if value:
                    self.credentials.set_secret(name, value)
                    self.providers[name].api_key = value
            self.preferences.save(values)
        except Exception as exc:
            QMessageBox.critical(self, "Could not save settings", str(exc)); return
        self.accept()
