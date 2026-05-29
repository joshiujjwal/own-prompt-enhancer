"""POST /v1/enhance and POST /v1/enhance/batch routes."""

from __future__ import annotations

import structlog
from fastapi import APIRouter, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.api.config import Settings, get_settings
from src.api.dependencies import get_enhancer
from src.enhancer.orchestrator import PromptEnhancer
from src.models.prompt import (
    BatchEnhancementRequest,
    BatchEnhancementResponse,
    EnhancementRequest,
    EnhancementResponse,
)

router = APIRouter(tags=["enhance"])
logger = structlog.get_logger()
limiter = Limiter(key_func=get_remote_address)


@router.post("/enhance", response_model=EnhancementResponse)
async def enhance_prompt(
    request: Request,
    body: EnhancementRequest,
    settings: Settings = Depends(get_settings),
    enhancer: PromptEnhancer = Depends(get_enhancer),
) -> EnhancementResponse:
    """Enhance a single raw prompt using the configured strategy."""
    enhanced, latency_ms = await enhancer.enhance(body.text)
    return EnhancementResponse(
        original=body.text,
        enhanced=enhanced,
        strategy_used=body.strategy,
        tokens_original=len(body.text.split()),
        tokens_enhanced=len(enhanced.split()),
        latency_ms=latency_ms,
    )


@router.post("/enhance/batch", response_model=BatchEnhancementResponse)
async def enhance_batch(
    request: Request,
    body: BatchEnhancementRequest,
    enhancer: PromptEnhancer = Depends(get_enhancer),
) -> BatchEnhancementResponse:
    """Enhance up to 20 prompts in one request."""
    results = []
    for item in body.prompts:
        enhanced, latency_ms = await enhancer.enhance(item.text)
        results.append(
            EnhancementResponse(
                original=item.text,
                enhanced=enhanced,
                strategy_used=item.strategy,
                tokens_original=len(item.text.split()),
                tokens_enhanced=len(enhanced.split()),
                latency_ms=latency_ms,
            )
        )
    return BatchEnhancementResponse(results=results)
