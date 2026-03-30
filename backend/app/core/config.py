"""
app/core/config.py
──────────────────
Centralised application settings loaded from environment variables
(or .env file via pydantic-settings).

Design decision: We use pydantic-settings instead of plain python-dotenv
because it provides automatic type coercion, field validation, and IDE
auto-completion while reading from .env.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Silently ignore env vars not declared as fields
    )

    # ── General ────────────────────────────────────────────────────────────────
    APP_NAME: str = "Lumora"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    # ── Security ───────────────────────────────────────────────────────────────
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Database ───────────────────────────────────────────────────────────────
    DATABASE_URL: str  # postgresql+asyncpg://...
    POSTGRES_DB: str = "lumora_db"

    # ── CORS ───────────────────────────────────────────────────────────────────
    ALLOWED_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            import json
            return json.loads(v)
        return v

    # ── Pagination ─────────────────────────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100


@lru_cache
def get_settings() -> Settings:
    """Cache the settings instance so it's only parsed once."""
    return Settings()


settings = get_settings()
