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

The project includes a safe workspace registry for Developer Mode. It allows projects to be created and file reads/writes to remain within the selected project root while rejecting path traversal attempts. This is a project-local guardrail for source code operations, not a full autonomous code editing system.

## Research mode

The repository includes a structured research-mode layer that keeps verified sources separate from interpretation. Research reports store citations, findings, and a final summary in a traceable format suitable for later review.

## Security and auditing

The application includes an append-only audit log for task states, approvals, and automation events to preserve a verifiable action history. Sensitive operations remain default-deny, and approvals are still task-scoped and expiring.

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
- Main command console and shared floating companion state

## Limitations

This does not complete the entire original roadmap. No end-to-end execution has been run in this tool session. Full Windows UI verification, provider credentials/network testing, hardware monitoring UI, executable approval integration, full desktop controls, file/project developer tools, research with source citations, and voice recognition/synthesis remain future work. Cancellation marks a task cancelled but cannot interrupt an in-flight HTTP request until the provider returns.
