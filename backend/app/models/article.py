"""
app/models/article.py
─────────────────────
Content system for the Stress & Overthinking module:
  - ArticleCategory (stress, anxiety, focus, …)
  - Article          (tips, guides)
"""
from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class ArticleCategory(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "article_categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)

    articles: Mapped[list["Article"]] = relationship("Article", back_populates="category")


class Article(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String(300), unique=True, index=True, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("article_categories.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    category: Mapped[Optional["ArticleCategory"]] = relationship(
        "ArticleCategory", back_populates="articles"
    )

    def __repr__(self) -> str:
        return f"<Article id={self.id} title={self.title!r}>"
