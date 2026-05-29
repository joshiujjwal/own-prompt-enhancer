"""Structure formatting strategy — converts a vague prompt into Goal/Context/Constraints blocks."""

from src.enhancer.strategies.base import BaseEnhancementStrategy


class StructureFormatterStrategy(BaseEnhancementStrategy):
    """Reformats prompt as Goal / Context / Constraints / Expected Output sections."""

    @property
    def strategy_id(self) -> str:
        return "structure_formatter"

    @property
    def description(self) -> str:
        return (
            "Wraps the prompt in structured sections: Goal, Context, Constraints, "
            "and Expected Output Format."
        )

    def enhance(self, raw: str) -> str:
        if not raw.strip():
            raise ValueError("Prompt must not be empty.")
        text = raw.strip()
        return (
            f"## Goal\n{text}\n\n"
            "## Context\n[Add relevant background information here]\n\n"
            "## Constraints\n[Specify any constraints, limitations, or requirements]\n\n"
            "## Expected Output Format\n[Describe the desired format, length, or structure of the response]"
        )
