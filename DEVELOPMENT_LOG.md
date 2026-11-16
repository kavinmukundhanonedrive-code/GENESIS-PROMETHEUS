# DEVELOPMENT LOG

## Current milestone

### Implemented
- Replaced placeholder model responses with HTTP integrations for Ollama, Gemini, and Groq.
- Added deterministic routing and sequential fallback; requests run on a worker thread in the PySide6 UI.
- Built the main command console with offline mode and cancellation surface.
- Added shared-state floating companion restore behavior.
- Hardened SQLite memory with project-scoped keys, parameterized search, and deletion.
- Added default-deny permission defaults and OS credential-store/environment secret retrieval.
- Replaced fake desktop actions with explicit executable-path launch and optional screenshot/window enumeration.
- Added focused offline tests and setup documentation.

### Not complete / not verified
- No local execution environment was available during this change; pytest and desktop startup have not been run.
- Worker cancellation is not yet cooperative at the HTTP request level; UI cancellation is a state marker only.
- Main-window provider connectivity polling and provider/model settings page are pending.
- The floating companion is a restore/status surface, not a fully synchronized command widget.
- Real desktop automation, screen perception, file manager, developer mode, research/citations, voice/wake-word, task persistence/recovery, and approval dialogs remain unimplemented.
- This project must not claim all original specification phases complete until these features are implemented and tested.

## Security decisions
- No API keys hardcoded or serialized to plaintext configuration files.
- Local providers are optional; offline requests never fall through to cloud providers.
- Launching accepts an explicit existing executable path and uses `shell=False`.
- Destructive operations and arbitrary command execution are intentionally unavailable.
