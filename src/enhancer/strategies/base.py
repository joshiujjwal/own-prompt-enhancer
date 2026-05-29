"""
OwnPromptEnhancer — base enhancement strategy.

All concrete strategies inherit from BaseEnhancementStrategy and implement `enhance`.
"""

from abc import ABC, abstractmethod


class BaseEnhancementStrategy(ABC):
    """Abstract base for all prompt enhancement strategies."""

    @property
    @abstractmethod
    def strategy_id(self) -> str:
        """Unique identifier used in the strategy registry."""

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description shown in GET /v1/strategies."""

    @abstractmethod
    def enhance(self, raw: str) -> str:
        """
        Enhance the raw prompt string.

        Args:
            raw: The original user prompt. Must be non-empty.

        Returns:
            The enhanced prompt string.

        Raises:
            ValueError: If raw is empty.
        """
