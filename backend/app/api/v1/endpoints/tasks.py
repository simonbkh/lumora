"""app/api/v1/endpoints/tasks.py – /tasks routes"""
from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Query, status
from fastapi.responses import Response

from app.core.dependencies import CurrentUserDep, SessionDep
from app.schemas.common import PagedResponse
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    data: TaskCreate,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> TaskRead:
    return await TaskService(session).create(current_user.id, data)


@router.get("/", response_model=PagedResponse[TaskRead])
async def list_tasks(
    current_user: CurrentUserDep,
    session: SessionDep,
    page: int = Query(default=1, ge=1),
    size: int = Query(default=20, ge=1, le=100),
) -> PagedResponse[TaskRead]:
    return await TaskService(session).list_my_tasks(current_user.id, page=page, size=size)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: UUID,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> TaskRead:
    return await TaskService(session).get(task_id, current_user.id)


@router.patch("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    data: TaskUpdate,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> TaskRead:
    return await TaskService(session).update(task_id, current_user.id, data)


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    current_user: CurrentUserDep,
    session: SessionDep,
) -> Response:
    await TaskService(session).delete(task_id, current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
