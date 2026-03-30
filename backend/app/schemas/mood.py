"""app/schemas/mood.py – Mood log schemas."""
from __future__ import annotations

import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class MoodLogCreate(BaseModel):
    rating: int = Field(ge=1, le=10)
    notes: Optional[str] = Field(default=None, max_length=1000)
    log_date: date


class MoodLogRead(BaseModel):
    id: uuid.UUID
    rating: int
    notes: Optional[str]
    log_date: date
    owner_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
