"""Unit tests for StructureFormatterStrategy."""

import pytest

from src.enhancer.strategies.structure_formatter import StructureFormatterStrategy


@pytest.fixture
def strategy() -> StructureFormatterStrategy:
    return StructureFormatterStrategy()


def test_structure_strategy_id(strategy: StructureFormatterStrategy) -> None:
    assert strategy.strategy_id == "structure_formatter"


def test_structure_contains_goal_section(strategy: StructureFormatterStrategy) -> None:
    result = strategy.enhance("explain REST APIs")
    assert "## Goal" in result


def test_structure_contains_context_section(strategy: StructureFormatterStrategy) -> None:
    result = strategy.enhance("explain REST APIs")
    assert "## Context" in result


def test_structure_contains_constraints_section(strategy: StructureFormatterStrategy) -> None:
    result = strategy.enhance("explain REST APIs")
    assert "## Constraints" in result


def test_structure_contains_output_format_section(strategy: StructureFormatterStrategy) -> None:
    result = strategy.enhance("explain REST APIs")
    assert "## Expected Output Format" in result


def test_structure_embeds_original_text(strategy: StructureFormatterStrategy) -> None:
    raw = "explain REST APIs"
    result = strategy.enhance(raw)
    assert raw in result


def test_structure_raises_on_empty(strategy: StructureFormatterStrategy) -> None:
    with pytest.raises(ValueError):
        strategy.enhance("")
