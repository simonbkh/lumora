"""app/services/article_service.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.article_repository import ArticleCategoryRepository, ArticleRepository
from app.schemas.article import (
    ArticleCategoryCreate, ArticleCategoryRead,
    ArticleCreate, ArticleRead, ArticleUpdate,
)
from app.schemas.common import PagedResponse


class ArticleCategoryService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ArticleCategoryRepository(session)

    async def create(self, data: ArticleCategoryCreate) -> ArticleCategoryRead:
        if await self._repo.get_by_slug(data.slug):
            raise ConflictException(f"Category slug '{data.slug}' already exists")
        cat = await self._repo.create(**data.model_dump())
        return ArticleCategoryRead.model_validate(cat)

    async def list(self, *, page: int = 1, size: int = 20) -> PagedResponse[ArticleCategoryRead]:
        items, total = await self._repo.list(offset=(page - 1) * size, limit=size)
        return PagedResponse.create(
            items=[ArticleCategoryRead.model_validate(i) for i in items],
            total=total, page=page, size=size,
        )


class ArticleService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ArticleRepository(session)

    async def create(self, data: ArticleCreate) -> ArticleRead:
        if await self._repo.get_by_slug(data.slug):
            raise ConflictException(f"Slug '{data.slug}' already exists")
        article = await self._repo.create(**data.model_dump())
        return ArticleRead.model_validate(article)

    async def list_published(self, *, page: int = 1, size: int = 20) -> PagedResponse[ArticleRead]:
        items, total = await self._repo.list_published(offset=(page - 1) * size, limit=size)
        return PagedResponse.create(
            items=[ArticleRead.model_validate(i) for i in items],
            total=total, page=page, size=size,
        )

    async def get_by_slug(self, slug: str) -> ArticleRead:
        article = await self._repo.get_by_slug(slug)
        if not article:
            raise NotFoundException("Article not found")
        return ArticleRead.model_validate(article)

    async def update(self, article_id: UUID, data: ArticleUpdate) -> ArticleRead:
        article = await self._repo.get_by_id(article_id)
        if not article:
            raise NotFoundException("Article not found")
        updated = await self._repo.update(article, **data.model_dump(exclude_none=True))
        return ArticleRead.model_validate(updated)

    async def delete(self, article_id: UUID) -> None:
        article = await self._repo.get_by_id(article_id)
        if not article:
            raise NotFoundException("Article not found")
        await self._repo.delete(article)
