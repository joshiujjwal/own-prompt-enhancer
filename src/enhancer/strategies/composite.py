"""Composite strategy — applies context_enricher → structure_formatter → cot_injector in sequence."""

from src.enhancer.strategies.base import BaseEnhancementStrategy
from src.enhancer.strategies.context_enricher import ContextEnricherStrategy
from src.enhancer.strategies.structure_formatter import StructureFormatterStrategy
from src.enhancer.strategies.cot_injector import CoTInjectorStrategy


class CompositeStrategy(BaseEnhancementStrategy):
    """Chains all three strategies for maximum prompt enrichment."""

    def __init__(self, domain: str | None = None) -> None:
        self._chain: list[BaseEnhancementStrategy] = [
            ContextEnricherStrategy(domain=domain),
            StructureFormatterStrategy(),
            CoTInjectorStrategy(),
        ]

    @property
    def strategy_id(self) -> str:
        return "composite"

    @property
    def description(self) -> str:
        return (
            "Applies all strategies in sequence: domain role framing, "
            "structured sections, and chain-of-thought scaffolding."
        )

    def enhance(self, raw: str) -> str:
        result = raw
        for strategy in self._chain:
            result = strategy.enhance(result)
        return result
