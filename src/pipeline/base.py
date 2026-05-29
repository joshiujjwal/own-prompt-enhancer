"""Base pipeline adapter interface."""

from abc import ABC, abstractmethod


class BasePipelineAdapter(ABC):
    """Abstract base for LLM-powered rewriting adapters."""

    @abstractmethod
    async def rewrite(self, prompt: str) -> str:
        """
        Rewrite the given prompt using the underlying LLM.

        Args:
            prompt: The strategy-enhanced prompt to further refine.

        Returns:
            The LLM-rewritten prompt.
        """
