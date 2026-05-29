"""Context enricher strategy — injects domain vocabulary and expert role framing."""

from src.enhancer.strategies.base import BaseEnhancementStrategy


class ContextEnricherStrategy(BaseEnhancementStrategy):
    """Prepends an expert role frame and domain context to the prompt."""

    def __init__(self, domain: str | None = None) -> None:
        self._domain = domain or "the relevant field"

    @property
    def strategy_id(self) -> str:
        return "context_enricher"

    @property
    def description(self) -> str:
        return (
            "Prepends an expert role declaration and domain context to improve "
            "the model's framing of the task."
        )

    def enhance(self, raw: str) -> str:
        if not raw.strip():
            raise ValueError("Prompt must not be empty.")
        role_prefix = (
            f"You are an expert in {self._domain}. "
            "Draw on your deep domain knowledge to provide a precise, thorough response."
        )
        return f"{role_prefix}\n\n{raw.strip()}"
