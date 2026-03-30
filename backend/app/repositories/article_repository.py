"""app/repositories/article_repository.py"""
from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.article import Article, ArticleCategory
from app.repositories.base_repository import BaseRepository


class ArticleCategoryRepository(BaseRepository[ArticleCategory]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(ArticleCategory, session)

    async def get_by_slug(self, slug: str) -> ArticleCategory | None:
        result = await self.session.execute(
            select(ArticleCategory).where(ArticleCategory.slug == slug)
        )
        return result.scalar_one_or_none()


class ArticleRepository(BaseRepository[Article]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Article, session)

    async def get_by_slug(self, slug: str) -> Article | None:
        result = await self.session.execute(
            select(Article).where(Article.slug == slug)
        )
        return result.scalar_one_or_none()

    async def list_published(self, *, offset: int = 0, limit: int = 20):
        return await self.list(
            offset=offset,
            limit=limit,
            filters=[Article.is_published.is_(True)],
            order_by=Article.created_at.desc(),
        )
