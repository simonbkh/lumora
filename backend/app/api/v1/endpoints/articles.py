"""app/api/v1/endpoints/articles.py – /articles routes"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response

from app.core.dependencies import SessionDep, require_roles
from app.models.user import RoleEnum
from app.schemas.article import (
    ArticleCategoryCreate, ArticleCategoryRead,
    ArticleCreate, ArticleRead, ArticleUpdate,
)
from app.schemas.common import PagedResponse
from app.services.article_service import ArticleCategoryService, ArticleService

router = APIRouter(prefix="/articles", tags=["Articles & Content"])

# ── Categories ────────────────────────────────────────────────────────────────

@router.post(
    "/categories",
    response_model=ArticleCategoryRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def create_category(data: ArticleCategoryCreate, session: SessionDep) -> ArticleCategoryRead:
    return await ArticleCategoryService(session).create(data)


@router.get("/categories", response_model=PagedResponse[ArticleCategoryRead])
async def list_categories(
    session: SessionDep, page: int = 1, size: int = 20
) -> PagedResponse[ArticleCategoryRead]:
    return await ArticleCategoryService(session).list(page=page, size=size)


# ── Articles ──────────────────────────────────────────────────────────────────

@router.post(
    "/",
    response_model=ArticleRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def create_article(data: ArticleCreate, session: SessionDep) -> ArticleRead:
    return await ArticleService(session).create(data)


@router.get("/", response_model=PagedResponse[ArticleRead])
async def list_articles(
    session: SessionDep, page: int = 1, size: int = 20
) -> PagedResponse[ArticleRead]:
    return await ArticleService(session).list_published(page=page, size=size)


@router.get("/{slug}", response_model=ArticleRead)
async def get_article(slug: str, session: SessionDep) -> ArticleRead:
    return await ArticleService(session).get_by_slug(slug)


@router.patch(
    "/{article_id}",
    response_model=ArticleRead,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def update_article(
    article_id: UUID, data: ArticleUpdate, session: SessionDep
) -> ArticleRead:
    return await ArticleService(session).update(article_id, data)


# Note: returning Response() directly bypasses FastAPI serialisation — correct for 204
@router.delete(
    "/{article_id}",
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def delete_article(article_id: UUID, session: SessionDep) -> Response:
    await ArticleService(session).delete(article_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
