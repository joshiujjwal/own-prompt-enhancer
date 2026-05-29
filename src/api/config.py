"""Pydantic Settings — reads from environment / .env file."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")

    adapter: Literal["openai", "anthropic", "local"] = Field(default="openai", alias="ADAPTER")
    local_model_path: str = Field(default="models/ope-v1/", alias="LOCAL_MODEL_PATH")

    max_prompt_length: int = Field(default=4096, alias="MAX_PROMPT_LENGTH")
    rate_limit: str = Field(default="60/minute", alias="RATE_LIMIT")
    allowed_origins: list[str] = Field(
        default=["http://localhost:5173"], alias="ALLOWED_ORIGINS"
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")


@lru_cache
def get_settings() -> Settings:
    return Settings()
