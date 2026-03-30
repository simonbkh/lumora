"""
app/repositories/base_repository.py
────────────────────────────────────
Generic async repository providing common CRUD operations.
All domain-specific repositories extend this class.

Design decision: A generic base keeps each repository DRY while still
allowing overrides for custom queries.
"""
from __future__ import annotations

from typing import Any, Generic, Sequence, Type, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: Type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, id: UUID) -> ModelT | None:
        result = await self.session.get(self.model, id)
        return result

    async def list(
        self,
        *,
        offset: int = 0,
        limit: int = 20,
        filters: list[Any] | None = None,
        order_by: Any | None = None,
    ) -> tuple[Sequence[ModelT], int]:
        """Return (items, total_count) for pagination."""
        stmt = select(self.model)
        count_stmt = select(func.count()).select_from(self.model)

        if filters:
            for f in filters:
                stmt = stmt.where(f)
                count_stmt = count_stmt.where(f)

        if order_by is not None:
            stmt = stmt.order_by(order_by)

        total_result = await self.session.execute(count_stmt)
        total: int = total_result.scalar_one()

        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all(), total

    async def create(self, **kwargs: Any) -> ModelT:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: ModelT, **kwargs: Any) -> ModelT:
        for key, value in kwargs.items():
            if value is not None:
                setattr(obj, key, value)
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def delete(self, obj: ModelT) -> None:
        await self.session.delete(obj)
        await self.session.flush()
