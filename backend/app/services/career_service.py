"""app/services/career_service.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.career_repository import (
    CareerPathRepository, ResourceRepository,
    SkillRepository, UserSkillRepository,
)
from app.schemas.career import (
    CareerPathCreate, CareerPathRead,
    ResourceCreate, ResourceRead,
    SkillCreate, SkillRead,
    UserSkillCreate, UserSkillRead, UserSkillUpdate,
)
from app.schemas.common import PagedResponse


class CareerPathService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = CareerPathRepository(session)

    async def create(self, data: CareerPathCreate) -> CareerPathRead:
        if await self._repo.get_by_slug(data.slug):
            raise ConflictException(f"Slug '{data.slug}' already exists")
        path = await self._repo.create(**data.model_dump())
        return CareerPathRead.model_validate(path)

    async def list(self, *, page: int = 1, size: int = 20) -> PagedResponse[CareerPathRead]:
        items, total = await self._repo.list(offset=(page - 1) * size, limit=size)
        return PagedResponse.create(
            items=[CareerPathRead.model_validate(i) for i in items],
            total=total, page=page, size=size,
        )


class ResourceService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = ResourceRepository(session)

    async def create(self, data: ResourceCreate) -> ResourceRead:
        resource = await self._repo.create(**data.model_dump())
        return ResourceRead.model_validate(resource)

    async def list_for_career(
        self, career_id: UUID, *, page: int = 1, size: int = 20
    ) -> PagedResponse[ResourceRead]:
        items, total = await self._repo.list_for_career(
            career_id, offset=(page - 1) * size, limit=size
        )
        return PagedResponse.create(
            items=[ResourceRead.model_validate(i) for i in items],
            total=total, page=page, size=size,
        )


class SkillService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = SkillRepository(session)

    async def create(self, data: SkillCreate) -> SkillRead:
        skill = await self._repo.create(**data.model_dump())
        return SkillRead.model_validate(skill)


class UserSkillService:
    def __init__(self, session: AsyncSession) -> None:
        self._repo = UserSkillRepository(session)

    async def add(self, user_id: UUID, data: UserSkillCreate) -> UserSkillRead:
        existing = await self._repo.get_user_skill(user_id, data.skill_id)
        if existing:
            raise ConflictException("Skill already added")
        us = await self._repo.create(user_id=user_id, **data.model_dump())
        return UserSkillRead.model_validate(us)

    async def update_progress(
        self, user_id: UUID, skill_id: UUID, data: UserSkillUpdate
    ) -> UserSkillRead:
        us = await self._repo.get_user_skill(user_id, skill_id)
        if not us:
            raise NotFoundException("User skill not found")
        updated = await self._repo.update(us, progress=data.progress)
        return UserSkillRead.model_validate(updated)

    async def list_mine(
        self, user_id: UUID, *, page: int = 1, size: int = 20
    ) -> PagedResponse[UserSkillRead]:
        items, total = await self._repo.list_for_user(
            user_id, offset=(page - 1) * size, limit=size
        )
        return PagedResponse.create(
            items=[UserSkillRead.model_validate(i) for i in items],
            total=total, page=page, size=size,
        )
