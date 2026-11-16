# Development log

## Provider settings and safety milestone

- Added Systems & Settings dialog with editable provider model IDs, secure keyring credential writes, and non-blocking provider connection checks.
- Added JSON persistence for model preferences only; credentials are explicitly excluded.
- Added task-scoped approval requests with expiry, explicit approve/deny, and one-time consumption.
- Added guarded task transitions, dependency checks, and thread-safe registry access.
- Updated UI to retain a worker pool, surface task errors, and distinguish cancellation state.
- Added tests for approval semantics and provider preference persistence.

## Verification

Tests were authored but not executed in this environment. Run `python -m pytest -q` after installing requirements. Provider checks require network access, configured keys, and/or a running Ollama service. Approval primitives are not yet wired to actual automation execution; dangerous operations remain unavailable by design.
