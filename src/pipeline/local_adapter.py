"""Local HuggingFace model adapter for offline prompt rewriting."""

from __future__ import annotations

from typing import Any

from src.pipeline.base import BasePipelineAdapter

INSTRUCTION = (
    "Rewrite the following prompt to be clearer, more structured, and more effective "
    "for a large language model. Return only the improved prompt.\n\nPrompt:\n"
)


class LocalAdapter(BasePipelineAdapter):
    """
    Rewrite adapter that loads a local HuggingFace model.

    Args:
        pipeline: A `transformers.pipeline` instance (text-generation).
        max_new_tokens: Maximum tokens to generate.
    """

    def __init__(self, pipeline: Any, max_new_tokens: int = 512) -> None:
        self._pipeline = pipeline
        self._max_new_tokens = max_new_tokens

    async def rewrite(self, prompt: str) -> str:
        instruction = f"{INSTRUCTION}{prompt}"
        result = self._pipeline(
            instruction,
            max_new_tokens=self._max_new_tokens,
            do_sample=False,
        )
        generated: str = result[0]["generated_text"]
        # Strip the instruction prefix if the model echoes it
        if generated.startswith(instruction):
            generated = generated[len(instruction):].strip()
        return generated or prompt
