from __future__ import annotations

from core.intelligence_router import IntelligenceRouter


def test_simple_routing() -> None:
    router = IntelligenceRouter()
    assert router.route("simple") == ["native"]


def test_development_routing() -> None:
    router = IntelligenceRouter()
    result = router.route("development")
    assert "native" in result
    assert "gemini" in result


def test_prompt_routing() -> None:
    router = IntelligenceRouter()
    result = router.route_for_prompt("Please debug this code issue.")
    assert "native" in result
    assert "gemini" in result
