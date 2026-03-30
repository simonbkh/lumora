"""app/services/mood_service.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.repositories.mood_repository import MoodRepository
from app.schemas.common import PagedResponse
from app.schemas.mood import MoodLogCreate, MoodLogRead


class MoodService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = MoodRepository(session)

    async def create(self, user_id: UUID, data: MoodLogCreate) -> MoodLogRead:
        log = await self._repo.create(owner_id=user_id, **data.model_dump())
        return MoodLogRead.model_validate(log)

    async def list_mine(
        self, user_id: UUID, *, page: int = 1, size: int = 20
    ) -> PagedResponse[MoodLogRead]:
        offset = (page - 1) * size
        logs, total = await self._repo.list_for_user(user_id, offset=offset, limit=size)
        return PagedResponse.create(
            items=[MoodLogRead.model_validate(l) for l in logs],
            total=total, page=page, size=size,
        )

    async def delete(self, log_id: UUID, user_id: UUID) -> None:
        log = await self._repo.get_by_id(log_id)
        if not log or log.owner_id != user_id:
            raise NotFoundException("Mood log not found")
        await self._repo.delete(log)
