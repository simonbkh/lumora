"""
app/main.py
───────────
FastAPI application factory.

Follows the "application factory" pattern so the app instance can be
imported by tests without starting the server.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        description="Youth Self-Development Platform API",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ── CORS ───────────────────────────────────────────────────────────────────
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.ALLOWED_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ──────────────────────────────────────────────────────
    register_exception_handlers(application)

    # ── Routes ─────────────────────────────────────────────────────────────────
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @application.get("/health", tags=["Health"])
    async def health_check() -> dict:
        return {"status": "ok", "app": settings.APP_NAME}

    return application


app = create_app()
