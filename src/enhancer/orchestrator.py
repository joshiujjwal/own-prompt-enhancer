"""
PromptEnhancer orchestrator — composes a strategy with an optional pipeline adapter.

Flow: raw prompt → strategy.enhance() → [adapter.rewrite() if set] → enhanced prompt
"""

from __future__ import annotations

import time

from src.enhancer.exceptions import PromptTooLongError
from src.enhancer.strategies.base import BaseEnhancementStrategy
from src.pipeline.base import BasePipelineAdapter

DEFAULT_MAX_LENGTH = 4096


class PromptEnhancer:
    """
    Orchestrates prompt enhancement.

    Args:
        strategy: The enhancement strategy to apply.
        adapter: Optional pipeline adapter for LLM-assisted rewriting.
        max_length: Maximum allowed prompt length (characters).
    """

    def __init__(
        self,
        strategy: BaseEnhancementStrategy,
        adapter: BasePipelineAdapter | None = None,
        max_length: int = DEFAULT_MAX_LENGTH,
    ) -> None:
        self._strategy = strategy
        self._adapter = adapter
        self._max_length = max_length

    async def enhance(self, raw: str) -> tuple[str, float]:
        """
        Enhance the raw prompt.

        Returns:
            Tuple of (enhanced_prompt, latency_ms).

        Raises:
            ValueError: If raw is empty.
            PromptTooLongError: If raw exceeds max_length.
        """
        if not raw.strip():
            raise ValueError("Prompt must not be empty.")
        if len(raw) > self._max_length:
            raise PromptTooLongError(len(raw), self._max_length)

        t0 = time.monotonic()
        result = self._strategy.enhance(raw)
        if self._adapter is not None:
            result = await self._adapter.rewrite(result)
        latency_ms = (time.monotonic() - t0) * 1000
        return result, latency_ms
