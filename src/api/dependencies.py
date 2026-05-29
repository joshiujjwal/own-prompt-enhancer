"""FastAPI dependency providers."""

from __future__ import annotations

from fastapi import Depends

from src.api.config import Settings, get_settings
from src.enhancer.orchestrator import PromptEnhancer
from src.enhancer.strategies import STRATEGY_REGISTRY


def get_enhancer(settings: Settings = Depends(get_settings)) -> PromptEnhancer:
    """
    Build a PromptEnhancer using the default 'composite' strategy and no adapter.

    In production, wire in the real adapter based on settings.adapter.
    Adapter initialisation is intentionally left for Phase 2 implementation.
    """
    strategy_class = STRATEGY_REGISTRY["composite"]
    strategy = strategy_class()  # type: ignore[call-arg]
    return PromptEnhancer(strategy=strategy, max_length=settings.max_prompt_length)
