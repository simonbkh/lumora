"""
tests/conftest.py
─────────────────
Pytest fixtures for async testing with an in-memory (or test) database.

Approach: We create a fresh SQLite (or test Postgres) engine per test session
and override the FastAPI `get_session` dependency to use a transactional
savepoint — ensuring each test is isolated and automatically rolled back.
"""
from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.base import Base
from app.db.session import get_session
from app.main import app

# Using an async SQLite in-memory DB for speed; swap for a real PG test DB in CI
TEST_DB_URL = "sqlite+aiosqlite:///./test.db"


@pytest_asyncio.fixture(scope="session")
async def engine():
    _engine = create_async_engine(TEST_DB_URL, echo=False)
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _engine
    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await _engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    """Each test gets a rolled-back transaction."""
    async with engine.connect() as conn:
        await conn.begin()
        async_session = async_sessionmaker(bind=conn, class_=AsyncSession, expire_on_commit=False)
        async with async_session() as s:
            yield s
        await conn.rollback()


@pytest_asyncio.fixture
async def client(session):
    """HTTP client with overridden DB session dependency."""
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
