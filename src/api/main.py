"""FastAPI application — lifespan, CORS, routes, exception handlers."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from src.api.config import get_settings
from src.api.routes import enhance, strategies
from src.enhancer.exceptions import AdapterError, OPEError, PromptTooLongError, UnknownStrategyError
from src.models.prompt import ErrorResponse

logger = structlog.get_logger()
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    settings = get_settings()
    await logger.ainfo("OwnPromptEnhancer starting", adapter=settings.adapter)
    yield
    await logger.ainfo("OwnPromptEnhancer shutting down")


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="OwnPromptEnhancer",
        description="SLM layer to improve prompts before passing to larger LLMs",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Rate limiting
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    @app.exception_handler(PromptTooLongError)
    async def prompt_too_long_handler(request: Request, exc: PromptTooLongError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                code="PROMPT_TOO_LONG",
                message=str(exc),
                details={"length": exc.length, "max_length": exc.max_length},
            ).model_dump(),
        )

    @app.exception_handler(UnknownStrategyError)
    async def unknown_strategy_handler(
        request: Request, exc: UnknownStrategyError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ErrorResponse(
                code="UNKNOWN_STRATEGY",
                message=str(exc),
                details={"strategy_id": exc.strategy_id},
            ).model_dump(),
        )

    @app.exception_handler(AdapterError)
    async def adapter_error_handler(request: Request, exc: AdapterError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content=ErrorResponse(
                code="ADAPTER_ERROR",
                message=str(exc),
                details={"adapter": exc.adapter},
            ).model_dump(),
        )

    # Routes
    app.include_router(enhance.router, prefix="/v1")
    app.include_router(strategies.router, prefix="/v1")

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
