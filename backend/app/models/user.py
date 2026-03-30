"""
app/models/user.py
──────────────────
User ORM model.

Roles are stored as a PostgreSQL-native Enum for constraint enforcement
at the DB level, not just in Python.
"""
from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Boolean, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.mood import MoodLog
    from app.models.task import Task
    from app.models.career import UserSkill


class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class User(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(150), nullable=False)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    goals: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="role_enum"), default=RoleEnum.USER, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relationships ──────────────────────────────────────────────────────────
    tasks: Mapped[List["Task"]] = relationship(
        "Task", back_populates="owner", cascade="all, delete-orphan"
    )
    mood_logs: Mapped[List["MoodLog"]] = relationship(
        "MoodLog", back_populates="owner", cascade="all, delete-orphan"
    )
    user_skills: Mapped[List["UserSkill"]] = relationship(
        "UserSkill", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
