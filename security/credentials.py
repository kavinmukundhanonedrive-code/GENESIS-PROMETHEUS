from __future__ import annotations

import os


class CredentialManager:
    """Reads secrets from OS credential storage when available, then environment.

    Secret writes intentionally require the optional `keyring` package; this class
    never writes plaintext .env files or logs credential material.
    """
    SERVICE = "GENESIS_PROMETHEUS"

    def get_secret(self, name: str) -> str:
        try:
            import keyring
            secret = keyring.get_password(self.SERVICE, name)
            if secret:
                return secret
        except Exception:
            pass
        env_name = {"gemini": "GEMINI_API_KEY", "groq": "GROQ_API_KEY"}.get(name.lower(), name.upper())
        return os.getenv(env_name, "")

    def set_secret(self, name: str, value: str) -> None:
        try:
            import keyring
        except ImportError as exc:
            raise RuntimeError("Install keyring to save secrets in the operating-system credential store.") from exc
        keyring.set_password(self.SERVICE, name, value)
