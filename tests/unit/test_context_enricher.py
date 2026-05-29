"""Unit tests for ContextEnricherStrategy."""

import pytest

from src.enhancer.strategies.context_enricher import ContextEnricherStrategy


def test_context_strategy_id() -> None:
    assert ContextEnricherStrategy().strategy_id == "context_enricher"


def test_context_injects_domain() -> None:
    strategy = ContextEnricherStrategy(domain="networking")
    result = strategy.enhance("explain DNS")
    assert "networking" in result


def test_context_injects_expert_role() -> None:
    strategy = ContextEnricherStrategy(domain="machine learning")
    result = strategy.enhance("explain transformers")
    assert "You are an expert" in result


def test_context_default_domain_fallback() -> None:
    strategy = ContextEnricherStrategy()
    result = strategy.enhance("explain anything")
    assert "You are an expert" in result


def test_context_preserves_original_prompt() -> None:
    strategy = ContextEnricherStrategy(domain="biology")
    raw = "explain CRISPR"
    result = strategy.enhance(raw)
    assert raw in result


def test_context_raises_on_empty() -> None:
    strategy = ContextEnricherStrategy()
    with pytest.raises(ValueError):
        strategy.enhance("")
