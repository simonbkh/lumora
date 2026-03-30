"""app/schemas/user.py – User request / response schemas."""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

from app.models.user import RoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=150)
    age: Optional[int] = Field(default=None, ge=13, le=120)
    goals: Optional[str] = Field(default=None, max_length=1000)


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(default=None, max_length=150)
    age: Optional[int] = Field(default=None, ge=13, le=120)
    goals: Optional[str] = Field(default=None, max_length=1000)


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    age: Optional[int]
    goals: Optional[str]
    role: RoleEnum
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str
