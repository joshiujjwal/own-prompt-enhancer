"""Anthropic-powered prompt rewriting adapter."""

from __future__ import annotations

import anthropic

from src.pipeline.base import BasePipelineAdapter

SYSTEM_PROMPT = (
    "You are a prompt engineering expert. "
    "You will receive a partially structured prompt. "
    "Your task is to refine it further: improve clarity, add missing context, "
    "sharpen constraints, and ensure it will elicit a high-quality response from a large language model. "
    "Return ONLY the improved prompt — no commentary, no preamble."
)


class AnthropicAdapter(BasePipelineAdapter):
    """Rewrite adapter backed by Anthropic Messages API."""

    def __init__(
        self,
        client: anthropic.AsyncAnthropic,
        model: str = "claude-haiku-3-5-20241022",
        max_tokens: int = 2048,
    ) -> None:
        self._client = client
        self._model = model
        self._max_tokens = max_tokens

    async def rewrite(self, prompt: str) -> str:
        message = await self._client.messages.create(
            model=self._model,
            max_tokens=self._max_tokens,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        block = message.content[0]
        if hasattr(block, "text"):
            return block.text  # type: ignore[no-any-return]
        return prompt
