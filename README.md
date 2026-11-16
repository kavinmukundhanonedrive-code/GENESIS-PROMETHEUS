# GENESIS PROMETHEUS

Windows-first desktop assistant with a deterministic Native Brain and optional Local (Ollama), Gemini, and Groq providers.

## Run

Python 3.10+:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
python main.py
```

## Provider configuration

The **Systems & Settings** dialog lets you change model names, save cloud credentials to the OS credential store, and run bounded connection checks off the UI thread. Credentials are loaded from Windows Credential Manager/macOS Keychain/Linux Secret Service through `keyring` when available, then from `GEMINI_API_KEY` / `GROQ_API_KEY`. Provider model preferences are stored in `data/provider_preferences.json`; secrets are never written there.

Ollama: install Ollama and pull a model (for example `ollama pull llama3.1`). Optional environment variables: `PROMETHEUS_OLLAMA_URL`, `PROMETHEUS_OLLAMA_MODEL`.

## Security and approvals

Permissions default to deny for desktop control, terminal execution, and file deletion. `security.approvals.ApprovalManager` creates expiring, task-scoped, one-use approvals and cannot itself execute actions. Actual automation callers must verify permissions and consume the matching approval before execution. No arbitrary shell execution or destructive file operation is exposed by this milestone.

## Current milestone

- Real HTTP provider adapters and deterministic fallback
- Offline requests are local-only
- Provider settings, model preference persistence, and async connection checks
- Thread-safe task registry and explicit state transitions/dependency gating
- Approval request lifecycle primitives
- SQLite persistent memory
- Main command console and shared floating companion state

## Limitations

This does not complete the entire original roadmap. No end-to-end execution has been run in this tool session. Full Windows UI verification, provider credentials/network testing, hardware monitoring UI, executable approval integration, full desktop controls, file/project developer tools, research with source citations, and voice recognition/synthesis remain future work. Cancellation marks a task cancelled but cannot interrupt an in-flight HTTP request until the provider returns.
