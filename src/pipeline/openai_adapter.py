"""OpenAI-powered prompt rewriting adapter."""

from __future__ import annotations

from openai import AsyncOpenAI

from src.pipeline.base import BasePipelineAdapter

SYSTEM_PROMPT = (
    "You are a prompt engineering expert. "
    "You will receive a partially structured prompt. "
    "Your task is to refine it further: improve clarity, add missing context, "
    "sharpen constraints, and ensure it will elicit a high-quality response from a large language model. "
    "Return ONLY the improved prompt — no commentary, no preamble."
)


class OpenAIAdapter(BasePipelineAdapter):
    """Rewrite adapter backed by OpenAI Chat Completions."""

    def __init__(
        self,
        client: AsyncOpenAI,
        model: str = "gpt-4o-mini",
        temperature: float = 0.3,
    ) -> None:
        self._client = client
        self._model = model
        self._temperature = temperature

    async def rewrite(self, prompt: str) -> str:
        response = await self._client.chat.completions.create(
            model=self._model,
            temperature=self._temperature,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        content = response.choices[0].message.content
        return content if content is not None else prompt
