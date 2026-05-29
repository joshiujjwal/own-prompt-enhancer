"""Chain-of-thought scaffolding injection strategy."""

from src.enhancer.strategies.base import BaseEnhancementStrategy


COT_SCAFFOLD = """
Think through this carefully, step by step:
1. First, identify the core question or task.
2. Consider relevant context, constraints, and assumptions.
3. Work through the problem methodically before providing your answer.
"""


class CoTInjectorStrategy(BaseEnhancementStrategy):
    """Appends a chain-of-thought scaffold to the prompt."""

    @property
    def strategy_id(self) -> str:
        return "cot_injector"

    @property
    def description(self) -> str:
        return (
            "Appends a chain-of-thought scaffold that instructs the model to "
            "reason step by step before answering."
        )

    def enhance(self, raw: str) -> str:
        if not raw.strip():
            raise ValueError("Prompt must not be empty.")
        return f"{raw.strip()}\n\n{COT_SCAFFOLD.strip()}"
