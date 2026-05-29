"""Unit tests for PromptEnhancer orchestrator."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.enhancer.exceptions import PromptTooLongError
from src.enhancer.orchestrator import PromptEnhancer
from src.enhancer.strategies.cot_injector import CoTInjectorStrategy


@pytest.fixture
def orchestrator() -> PromptEnhancer:
    return PromptEnhancer(strategy=CoTInjectorStrategy(), max_length=100)


async def test_orchestrator_returns_enhanced_string(orchestrator: PromptEnhancer) -> None:
    result, latency = await orchestrator.enhance("what is a linked list")
    assert "linked list" in result
    assert "step by step" in result.lower()
    assert latency >= 0


async def test_orchestrator_raises_on_empty(orchestrator: PromptEnhancer) -> None:
    with pytest.raises(ValueError):
        await orchestrator.enhance("")


async def test_orchestrator_raises_on_too_long(orchestrator: PromptEnhancer) -> None:
    with pytest.raises(PromptTooLongError):
        await orchestrator.enhance("a" * 101)


async def test_orchestrator_calls_adapter_when_set() -> None:
    mock_adapter = AsyncMock()
    mock_adapter.rewrite = AsyncMock(return_value="adapter-rewritten-prompt")
    enhancer = PromptEnhancer(
        strategy=CoTInjectorStrategy(),
        adapter=mock_adapter,
        max_length=4096,
    )
    result, _ = await enhancer.enhance("write a sorting algorithm")
    mock_adapter.rewrite.assert_called_once()
    assert result == "adapter-rewritten-prompt"


async def test_orchestrator_skips_adapter_when_none() -> None:
    enhancer = PromptEnhancer(strategy=CoTInjectorStrategy(), adapter=None)
    result, _ = await enhancer.enhance("what is memoization")
    assert "memoization" in result
