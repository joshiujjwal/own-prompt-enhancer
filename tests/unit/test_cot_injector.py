"""Unit tests for CoTInjectorStrategy."""

import pytest

from src.enhancer.strategies.cot_injector import CoTInjectorStrategy


@pytest.fixture
def strategy() -> CoTInjectorStrategy:
    return CoTInjectorStrategy()


def test_cot_strategy_id(strategy: CoTInjectorStrategy) -> None:
    assert strategy.strategy_id == "cot_injector"


def test_cot_appends_scaffold(strategy: CoTInjectorStrategy) -> None:
    result = strategy.enhance("what is recursion")
    assert "what is recursion" in result
    assert "step by step" in result.lower()


def test_cot_preserves_original_text(strategy: CoTInjectorStrategy) -> None:
    raw = "explain the difference between TCP and UDP"
    result = strategy.enhance(raw)
    assert result.startswith(raw)


def test_cot_raises_on_empty(strategy: CoTInjectorStrategy) -> None:
    with pytest.raises(ValueError, match="empty"):
        strategy.enhance("")


def test_cot_raises_on_whitespace_only(strategy: CoTInjectorStrategy) -> None:
    with pytest.raises(ValueError):
        strategy.enhance("   ")


def test_cot_strips_leading_trailing_whitespace(strategy: CoTInjectorStrategy) -> None:
    result = strategy.enhance("  what is python  ")
    assert result.startswith("what is python")
