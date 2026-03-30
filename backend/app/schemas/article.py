"""app/schemas/article.py – Article and category schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ArticleCategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None
    slug: str = Field(min_length=1, max_length=120)


class ArticleCategoryRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    slug: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ArticleCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str
    slug: str = Field(min_length=1, max_length=300)
    summary: Optional[str] = Field(default=None, max_length=500)
    is_published: bool = False
    category_id: Optional[uuid.UUID] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    is_published: Optional[bool] = None
    category_id: Optional[uuid.UUID] = None


class ArticleRead(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    slug: str
    summary: Optional[str]
    is_published: bool
    category_id: Optional[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
