# GENESIS PROMETHEUS

Windows-first desktop intelligence application with a deterministic Native Brain and optional Local (Ollama), Gemini, and Groq providers.

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

The Systems & Settings dialog lets you change model names, save cloud credentials to the OS credential store, and run bounded connection checks off the UI thread. Credentials are loaded from the OS credential store through `keyring` when available, then from `GEMINI_API_KEY` / `GROQ_API_KEY`. Provider model preferences are stored in `data/provider_preferences.json`; secrets are never written there.

Ollama: install Ollama and pull a model (for example `ollama pull llama3.1`). Optional environment variables: `PROMETHEUS_OLLAMA_URL`, `PROMETHEUS_OLLAMA_MODEL`.

## Developer workspace

The project includes a safe workspace registry for Developer Mode. It allows projects to be created and file reads/writes to remain within the selected project root while rejecting path traversal attempts.

## Research mode

The repository includes a structured research-mode layer that keeps verified sources separate from interpretation. Research reports store citations, findings, and a final summary in traceable format.

## Security, approvals, and execution verification

This milestone adds a dedicated execution ledger and action guard. Every significant task execution is recorded locally with state, summary, provider, timing, and outcome metadata. Sensitive automation actions now use a permission gate that requires explicit approval before they are marked as consumable. This creates a stronger safety boundary without enabling arbitrary automation yet.

## Current milestone

- Real HTTP provider adapters and deterministic fallback
- Offline requests are local-only
- Provider settings, model preference persistence, and async connection checks
- Thread-safe task registry and explicit state transitions/dependency gating
- Approval request lifecycle primitives
- SQLite persistent memory
- Developer workspace isolation for project-aware file operations
- Structured research reporting with citations and fact/interpretation separation
- Append-only security audit logging
- Local execution history and permission-gated action enforcement
- Main command console and shared floating companion state

## Limitations

This remains an incremental engineering foundation. Full Windows UI verification, provider credentials/network testing, hardware monitoring UI, real desktop controls, developer workspace editing, research with source collection, voice interaction, and full product polish remain future work.
