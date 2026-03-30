"""app/schemas/career.py – Career path, resource, and skill schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# ── Career Path ───────────────────────────────────────────────────────────────

class CareerPathCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: Optional[str] = None
    slug: str = Field(min_length=1, max_length=180)


class CareerPathRead(BaseModel):
    id: uuid.UUID
    name: str
    description: Optional[str]
    slug: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Resource ──────────────────────────────────────────────────────────────────

class ResourceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    url: Optional[str] = None
    content: Optional[str] = None
    resource_type: str = Field(default="link", max_length=50)
    career_path_id: uuid.UUID


class ResourceRead(BaseModel):
    id: uuid.UUID
    title: str
    url: Optional[str]
    content: Optional[str]
    resource_type: str
    career_path_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Skill ─────────────────────────────────────────────────────────────────────

class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    career_path_id: uuid.UUID


class SkillRead(BaseModel):
    id: uuid.UUID
    name: str
    career_path_id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}


# ── UserSkill ─────────────────────────────────────────────────────────────────

class UserSkillCreate(BaseModel):
    skill_id: uuid.UUID
    progress: int = Field(default=0, ge=0, le=100)


class UserSkillUpdate(BaseModel):
    progress: int = Field(ge=0, le=100)


class UserSkillRead(BaseModel):
    id: uuid.UUID
    skill_id: uuid.UUID
    progress: int
    created_at: datetime

    model_config = {"from_attributes": True}
