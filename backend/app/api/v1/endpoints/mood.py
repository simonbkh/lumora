"""app/api/v1/endpoints/mood.py – /mood routes"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, status
from fastapi.responses import Response

from app.core.dependencies import CurrentUserDep, SessionDep
from app.schemas.common import PagedResponse
from app.schemas.mood import MoodLogCreate, MoodLogRead
from app.services.mood_service import MoodService

router = APIRouter(prefix="/mood", tags=["Mood Tracking"])


@router.post("/", response_model=MoodLogRead, status_code=status.HTTP_201_CREATED)
async def create_log(
    data: MoodLogCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> MoodLogRead:
    return await MoodService(session).create(current_user.id, data)


@router.get("/", response_model=PagedResponse[MoodLogRead])
async def list_logs(
    current_user: CurrentUserDep,
    session: SessionDep,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> PagedResponse[MoodLogRead]:
    return await MoodService(session).list_mine(current_user.id, page=page, size=size)


@router.delete("/{log_id}")
async def delete_log(
    log_id: UUID,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> Response:
    await MoodService(session).delete(log_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
