# GENESIS PROMETHEUS

GENESIS PROMETHEUS is a desktop intelligence platform built around a four-brain orchestration model:

- Native Brain: deterministic coordination layer
- Local Brain: local reasoning and private processing via Ollama
- Gemini Brain: Google Gemini provider integration
- Groq Brain: Groq inference service integration

This repository now contains a strong Phase 1-6 foundation: architecture, orchestration, provider adapters, memory persistence, UI shell, automation scaffolding, security, systems monitoring, voice service, and tests.

## Architecture overview

The project is designed around a modular backend architecture where the Native Brain remains the single control authority. All external intelligence services are abstracted behind provider adapters and treated as assistant providers rather than autonomous system controllers.

## Design principles

1. Native Brain remains the orchestration authority.
2. Provider adapters are isolated behind a common interface.
3. Task management is centralized and observable.
4. Memory is persistent and independent from providers.
5. UI and automation share a common backend state.
6. The floating widget is a shared-state companion mode, not a second AI.
7. Local operation remains possible without cloud access.

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
│   ├── intelligence_router.py
│   ├── state.py
│   └── task_manager.py
├── providers/
│   ├── __init__.py
│   ├── base_provider.py
│   ├── local_provider.py
│   ├── gemini_provider.py
│   └── groq_provider.py
├── memory/
│   ├── __init__.py
│   ├── database.py
│   └── repository.py
├── ui/
│   ├── __init__.py
│   ├── styles.py
│   ├── main_window.py
│   └── floating_widget.py
├── automation/
│   ├── __init__.py
│   └── desktop_controller.py
├── security/
│   ├── __init__.py
│   ├── credentials.py
│   └── permissions.py
├── monitoring/
│   ├── __init__.py
│   └── system.py
├── voice/
│   ├── __init__.py
│   └── voice_service.py
├── tests/
│   ├── test_task_manager.py
│   ├── test_router.py
│   └── test_memory.py
├── data/
└── generated/
```

## Included functionality

- Central task manager with lifecycle states
- Native Brain orchestration shell
- Four-brain routing strategy
- Local, Gemini, and Groq provider adapters
- SQLite-backed memory store
- Shared application state model
- PySide6 shell scaffolding for main and floating UI
- Desktop automation interfaces
- Security and credential helpers
- System monitoring interfaces
- Voice service stubs
- Automated tests covering core logic

## Development status

This project is now at a robust engineering foundation stage. The architecture is in place and the major subsystems are defined. The remaining work is incremental productization: wiring actual services, hardening security, tuning UI behavior, and completing automation validation.

## Next steps

1. Connect real provider APIs with secure configuration
2. Build the operational UI with real task state binding
3. Add persistence and retrieval workflows for project memory
4. Implement approval workflows and destructive-action safeguards
5. Add actual desktop automation and validation controllers
6. Expand diagnostics and recovery behavior

## Important note

The system is intentionally designed to operate without cloud access and to remain maintainable. It keeps orchestration logic independent from provider-specific implementations to preserve deterministic control.
