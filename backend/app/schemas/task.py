"""app/schemas/task.py – Task request / response schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task import PriorityEnum, StatusEnum


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=2000)
    priority: PriorityEnum = PriorityEnum.MEDIUM
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=255)
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    deadline: Optional[datetime] = None
    is_completed: Optional[bool] = None


class TaskRead(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    priority: PriorityEnum
    status: StatusEnum
    deadline: Optional[datetime]
    is_completed: bool
    owner_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
