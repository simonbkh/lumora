"""app/repositories/mood_repository.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.mood import MoodLog
from app.repositories.base_repository import BaseRepository


class MoodRepository(BaseRepository[MoodLog]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(MoodLog, session)

    async def list_for_user(self, user_id: UUID, *, offset: int = 0, limit: int = 20):
        return await self.list(
            offset=offset,
            limit=limit,
            filters=[MoodLog.owner_id == user_id],
            order_by=MoodLog.log_date.desc(),
        )
