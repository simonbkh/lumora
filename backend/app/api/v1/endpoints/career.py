"""app/api/v1/endpoints/career.py – /career routes"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import CurrentUserDep, SessionDep, require_roles
from app.models.user import RoleEnum
from app.schemas.career import (
    CareerPathCreate, CareerPathRead,
    ResourceCreate, ResourceRead,
    SkillCreate, SkillRead,
    UserSkillCreate, UserSkillRead, UserSkillUpdate,
)
from app.schemas.common import PagedResponse
from app.services.career_service import (
    CareerPathService, ResourceService, SkillService, UserSkillService,
)

router = APIRouter(prefix="/career", tags=["Career Development"])

# ── Career Paths ──────────────────────────────────────────────────────────────

@router.post(
    "/paths",
    response_model=CareerPathRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def create_path(data: CareerPathCreate, session: SessionDep) -> CareerPathRead:
    return await CareerPathService(session).create(data)


@router.get("/paths", response_model=PagedResponse[CareerPathRead])
async def list_paths(
    session: SessionDep,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PagedResponse[CareerPathRead]:
    return await CareerPathService(session).list(page=page, size=size)


# ── Resources ─────────────────────────────────────────────────────────────────

@router.post(
    "/resources",
    response_model=ResourceRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def create_resource(data: ResourceCreate, session: SessionDep) -> ResourceRead:
    return await ResourceService(session).create(data)


@router.get("/paths/{career_id}/resources", response_model=PagedResponse[ResourceRead])
async def list_resources(
    career_id: UUID,
    session: SessionDep,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PagedResponse[ResourceRead]:
    return await ResourceService(session).list_for_career(career_id, page=page, size=size)


# ── Skills ────────────────────────────────────────────────────────────────────

@router.post(
    "/skills",
    response_model=SkillRead,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def create_skill(data: SkillCreate, session: SessionDep) -> SkillRead:
    return await SkillService(session).create(data)


# ── User Skills ───────────────────────────────────────────────────────────────

@router.post("/me/skills", response_model=UserSkillRead, status_code=status.HTTP_201_CREATED)
async def add_my_skill(
    data: UserSkillCreate, current_user: CurrentUserDep, session: SessionDep
) -> UserSkillRead:
    return await UserSkillService(session).add(current_user.id, data)


@router.get("/me/skills", response_model=PagedResponse[UserSkillRead])
async def list_my_skills(
    current_user: CurrentUserDep,
    session: SessionDep,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> PagedResponse[UserSkillRead]:
    return await UserSkillService(session).list_mine(current_user.id, page=page, size=size)


@router.patch("/me/skills/{skill_id}", response_model=UserSkillRead)
async def update_skill_progress(
    skill_id: UUID,
    data: UserSkillUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> UserSkillRead:
    return await UserSkillService(session).update_progress(current_user.id, skill_id, data)
