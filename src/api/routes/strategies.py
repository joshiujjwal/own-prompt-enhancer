"""GET /v1/strategies route."""

from __future__ import annotations

from fastapi import APIRouter

from src.enhancer.strategies import STRATEGY_REGISTRY
from src.models.prompt import StrategyInfo

router = APIRouter(tags=["strategies"])

# Static descriptions — keep in sync with strategy classes
_STRATEGY_EXAMPLES: dict[str, tuple[str, str]] = {
    "cot_injector": (
        "explain transformers",
        "explain transformers\n\nThink through this carefully, step by step:\n1. ...",
    ),
    "structure_formatter": (
        "explain transformers",
        "## Goal\nexplain transformers\n\n## Context\n...\n\n## Constraints\n...",
    ),
    "context_enricher": (
        "explain transformers",
        "You are an expert in machine learning. ...\n\nexplain transformers",
    ),
    "composite": (
        "explain transformers",
        "You are an expert... ## Goal\nexplain transformers\n\n## Context\n...\n\nThink step by step...",
    ),
}


@router.get("/strategies", response_model=list[StrategyInfo])
async def list_strategies() -> list[StrategyInfo]:
    """Return all available enhancement strategies with descriptions and examples."""
    results = []
    for strategy_id, strategy_class in STRATEGY_REGISTRY.items():
        instance = strategy_class()  # type: ignore[call-arg]
        before, after = _STRATEGY_EXAMPLES.get(strategy_id, ("example prompt", "enhanced prompt"))
        results.append(
            StrategyInfo(
                id=strategy_id,  # type: ignore[arg-type]
                name=strategy_id.replace("_", " ").title(),
                description=instance.description,
                example_before=before,
                example_after=after,
            )
        )
    return results
