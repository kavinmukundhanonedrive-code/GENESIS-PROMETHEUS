# GENESIS PROMETHEUS

GENESIS PROMETHEUS is a desktop intelligence platform built around a four-brain orchestration model:

- Native Brain: deterministic coordination layer
- Local Brain: Ollama-powered local reasoning
- Gemini Brain: Google Gemini provider integration
- Groq Brain: Groq inference provider integration

The inaugural foundation establishes a maintainable project structure, a central task manager, a Native Brain orchestration layer, and a secure configuration model.

## Architecture overview

This project starts with a modular backend architecture that keeps provider logic independent from orchestration logic.

### Core principles

1. Native Brain remains the control authority.
2. Provider adapters are isolated behind a common interface.
3. Tasks are tracked centrally with explicit state transitions.
4. UI state and automation state are shared, not duplicated.
5. Local operation remains possible without cloud access.

## Project structure

```text
GENESIS_PROMETHEUS/
├── main.py
├── requirements.txt
├── README.md
├── DEVELOPMENT_LOG.md
├── .gitignore
├── config/
│   ├── __init__.py
│   └── settings.py
├── core/
│   ├── __init__.py
│   ├── native_brain.py
│   └── task_manager.py
├── providers/
│   ├── __init__.py
│   └── base_provider.py
├── tests/
│   └── test_task_manager.py
└── data/
```

## Current status

This repository now contains the Phase 1 foundation:

- project structure
- configuration system
- task manager
- Native Brain orchestration skeleton
- provider interface abstraction
- test scaffolding

## Next incremental work

Planned next phases:

1. Add provider adapters for Local, Gemini, and Groq
2. Add SQLite-backed memory layer
3. Build the main PySide6 desktop shell
4. Add floating widget mode with shared backend state
5. Implement desktop automation modules
6. Add diagnostics, logs, approvals, and security controls

## Development note

This foundation intentionally prioritizes maintainability and correctness over a flashy demo. It is designed to support the architecture described in the project specification without creating fragile early-stage coupling.
