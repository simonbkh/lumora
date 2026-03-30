"""app/services/task_service.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ForbiddenException, NotFoundException
from app.repositories.task_repository import TaskRepository
from app.schemas.common import PagedResponse
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate


class TaskService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = TaskRepository(session)

    async def create(self, user_id: UUID, data: TaskCreate) -> TaskRead:
        task = await self._repo.create(
            owner_id=user_id,
            **data.model_dump(),
        )
        return TaskRead.model_validate(task)

    async def list_my_tasks(
        self, user_id: UUID, *, page: int = 1, size: int = 20
    ) -> PagedResponse[TaskRead]:
        offset = (page - 1) * size
        tasks, total = await self._repo.list_for_user(user_id, offset=offset, limit=size)
        return PagedResponse.create(
            items=[TaskRead.model_validate(t) for t in tasks],
            total=total,
            page=page,
            size=size,
        )

    async def get(self, task_id: UUID, user_id: UUID) -> TaskRead:
        task = await self._repo.get_by_id(task_id)
        if not task:
            raise NotFoundException("Task not found")
        if task.owner_id != user_id:
            raise ForbiddenException("Not your task")
        return TaskRead.model_validate(task)

    async def update(self, task_id: UUID, user_id: UUID, data: TaskUpdate) -> TaskRead:
        task = await self._repo.get_by_id(task_id)
        if not task:
            raise NotFoundException("Task not found")
        if task.owner_id != user_id:
            raise ForbiddenException("Not your task")
        updated = await self._repo.update(task, **data.model_dump(exclude_none=True))
        return TaskRead.model_validate(updated)

    async def delete(self, task_id: UUID, user_id: UUID) -> None:
        task = await self._repo.get_by_id(task_id)
        if not task:
            raise NotFoundException("Task not found")
        if task.owner_id != user_id:
            raise ForbiddenException("Not your task")
        await self._repo.delete(task)
