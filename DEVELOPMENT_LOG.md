# Development log

## Security and audit milestone

- Added an append-only SQLite audit log for task events, security approvals, and automation actions.
- Kept audit records fully local and separate from provider secrets.
- Continued Developer Mode sandboxing, research reporting, and approval lifecycle guardrails.
- Added a focused test for audit log persistence and retrieval.

## Verification

Tests were authored but not executed in this environment. Run `python -m pytest -q` after installing requirements. Provider checks require network access, configured keys, and/or a running Ollama service. Approval primitives are not yet wired to actual automation execution; dangerous operations remain unavailable by design.
