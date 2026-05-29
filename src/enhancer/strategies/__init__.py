"""Strategy registry — maps strategy IDs to their classes."""

from src.enhancer.strategies.base import BaseEnhancementStrategy
from src.enhancer.strategies.cot_injector import CoTInjectorStrategy
from src.enhancer.strategies.structure_formatter import StructureFormatterStrategy
from src.enhancer.strategies.context_enricher import ContextEnricherStrategy
from src.enhancer.strategies.composite import CompositeStrategy

STRATEGY_REGISTRY: dict[str, type[BaseEnhancementStrategy]] = {
    "cot_injector": CoTInjectorStrategy,
    "structure_formatter": StructureFormatterStrategy,
    "context_enricher": ContextEnricherStrategy,
    "composite": CompositeStrategy,
}

__all__ = [
    "BaseEnhancementStrategy",
    "CoTInjectorStrategy",
    "StructureFormatterStrategy",
    "ContextEnricherStrategy",
    "CompositeStrategy",
    "STRATEGY_REGISTRY",
]
