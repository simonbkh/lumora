"""app/api/v1/endpoints/users.py – /users routes"""
from __future__ import annotations

from fastapi import APIRouter, Depends, status

from app.core.dependencies import CurrentUserDep, SessionDep, require_roles
from app.models.user import RoleEnum
from app.schemas.common import PagedResponse
from app.schemas.user import UserRead, UserUpdate
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
async def get_me(current_user: CurrentUserDep) -> UserRead:
    """Return the authenticated user's profile."""
    return UserRead.model_validate(current_user)


@router.patch("/me", response_model=UserRead)
async def update_me(
    data: UserUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> UserRead:
    """Update the authenticated user's profile."""
    repo = UserRepository(session)
    updated = await repo.update(current_user, **data.model_dump(exclude_none=True))
    return UserRead.model_validate(updated)


@router.get(
    "/",
    response_model=PagedResponse[UserRead],
    dependencies=[Depends(require_roles(RoleEnum.ADMIN))],
)
async def list_users(
    session: SessionDep,
    page: int = 1,
    size: int = 20,
) -> PagedResponse[UserRead]:
    """[ADMIN] List all users with pagination."""
    repo = UserRepository(session)
    users, total = await repo.list(offset=(page - 1) * size, limit=size)
    return PagedResponse.create(
        items=[UserRead.model_validate(u) for u in users],
        total=total,
        page=page,
        size=size,
    )
