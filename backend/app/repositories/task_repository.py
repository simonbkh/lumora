"""app/repositories/task_repository.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.repositories.base_repository import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Task, session)

    async def list_for_user(
        self,
        user_id: UUID,
        *,
        offset: int = 0,
        limit: int = 20,
    ):
        return await self.list(
            offset=offset,
            limit=limit,
            filters=[Task.owner_id == user_id],
            order_by=Task.created_at.desc(),
        )
