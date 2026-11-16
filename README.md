# GENESIS PROMETHEUS

A Windows-first desktop intelligence application with a deterministic Native Brain and optional Local (Ollama), Gemini, and Groq providers.

## Run

Python 3.10+ is recommended. From the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On Linux/macOS, activate the virtual environment with its platform-specific command and run `python main.py`.

## Configure providers

- **Ollama:** install/start Ollama, pull a model (`ollama pull llama3.1`), set `PROMETHEUS_OLLAMA_URL` and `PROMETHEUS_OLLAMA_MODEL` if needed.
- **Gemini:** set `GEMINI_API_KEY`; optional `PROMETHEUS_GEMINI_MODEL`.
- **Groq:** set `GROQ_API_KEY`; optional `PROMETHEUS_GROQ_MODEL`.

For the current shell, for example:

```powershell
$env:GEMINI_API_KEY = "your-key"
$env:GROQ_API_KEY = "your-key"
```

Keys are not stored in source code or written to `.env`. The credential manager can use the OS credential store through `keyring`.

## What works in this milestone

- PySide6 command center; provider calls run off the UI thread.
- Rule-based request routing and sequential provider fallback.
- Real Ollama `/api/tags` and `/api/generate` calls.
- Real Gemini `generateContent` and Groq chat-completion requests.
- Explicit no-provider/offline messages (the application does not fabricate generated answers).
- SQLite persistent memory repository.
- Shared state used by the floating companion and main window.
- Conservative desktop helpers; launching requires a full executable path and uses `shell=False`.
- Test coverage for routing, task transitions, and memory persistence.

## Safety and current limitations

This is an early desktop application, not an autonomous unrestricted operator. Arbitrary shell/script execution, destructive file operations, mouse/keyboard control, wake-word listening, speech recognition/synthesis, web research/citations, and developer workspace editing are not enabled. These need explicit approval design, platform-specific implementations, and end-to-end testing before being advertised as complete. Provider selection and responses do not grant permissions. Desktop actions should be initiated only through a future explicit approval flow.

The floating companion currently restores the shared main session; it is not yet a full mini command console. Provider status is shown as configured/connected based on the last completed request, not continuously polled. There is no hardware in this repository environment to validate Windows desktop behavior.

## Tests

```powershell
python -m pytest -q
```

Tests are offline and do not require provider credentials. This repository change was not executed in a Python environment, so test results must be verified locally/CI.

## Architecture

- `core/native_brain.py`: orchestrates tasks; external models cannot take control.
- `core/intelligence_router.py`: deterministic workload routing.
- `providers/`: provider-specific HTTP adapters.
- `memory/`: SQLite persistence.
- `ui/`: PySide6 main and floating presentation.
- `security/`: permission and credential foundations.
- `automation/`: deliberately constrained desktop helpers.

See `DEVELOPMENT_LOG.md` for completed work and remaining roadmap.
