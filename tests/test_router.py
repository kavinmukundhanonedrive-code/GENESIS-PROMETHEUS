from __future__ import annotations

from core.intelligence_router import IntelligenceRouter


def test_simple_routing() -> None:
    assert IntelligenceRouter().route("simple") == ["native"]


def test_development_routing() -> None:
    result = IntelligenceRouter().route("development")
    assert result[0] == "local" and "gemini" in result


def test_prompt_routing() -> None:
    assert "gemini" in IntelligenceRouter().route_for_prompt("Please debug this code issue.")


def test_offline_never_routes_to_cloud() -> None:
    assert IntelligenceRouter().route("research", offline_mode=True) == ["local"]
