"""app/repositories/career_repository.py"""
from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.career import CareerPath, Resource, Skill, UserSkill
from app.repositories.base_repository import BaseRepository


class CareerPathRepository(BaseRepository[CareerPath]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CareerPath, session)

    async def get_by_slug(self, slug: str) -> CareerPath | None:
        result = await self.session.execute(
            select(CareerPath).where(CareerPath.slug == slug)
        )
        return result.scalar_one_or_none()


class ResourceRepository(BaseRepository[Resource]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Resource, session)

    async def list_for_career(self, career_path_id: UUID, *, offset: int = 0, limit: int = 20):
        return await self.list(
            offset=offset,
            limit=limit,
            filters=[Resource.career_path_id == career_path_id],
        )


class SkillRepository(BaseRepository[Skill]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Skill, session)


class UserSkillRepository(BaseRepository[UserSkill]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(UserSkill, session)

    async def get_user_skill(self, user_id: UUID, skill_id: UUID) -> UserSkill | None:
        result = await self.session.execute(
            select(UserSkill).where(
                UserSkill.user_id == user_id,
                UserSkill.skill_id == skill_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_for_user(self, user_id: UUID, *, offset: int = 0, limit: int = 20):
        return await self.list(
            offset=offset,
            limit=limit,
            filters=[UserSkill.user_id == user_id],
        )
