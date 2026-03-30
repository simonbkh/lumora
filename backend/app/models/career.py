"""
app/models/career.py
────────────────────
Career Development module:
  - CareerPath  (software, marketing, design, …)
  - Resource    (articles/links tied to a career path)
  - Skill       (global skill catalogue)
  - UserSkill   (association table: user <-> skill + progress level)
"""
from __future__ import annotations

import uuid
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class CareerPath(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "career_paths"

    name: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)

    resources: Mapped[list["Resource"]] = relationship(
        "Resource", back_populates="career_path", cascade="all, delete-orphan"
    )
    skills: Mapped[list["Skill"]] = relationship(
        "Skill", back_populates="career_path", cascade="all, delete-orphan"
    )


class Resource(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "resources"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(2048), nullable=True)
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), default="link", nullable=False)

    career_path_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("career_paths.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    career_path: Mapped["CareerPath"] = relationship("CareerPath", back_populates="resources")


class Skill(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "skills"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    career_path_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("career_paths.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    career_path: Mapped["CareerPath"] = relationship("CareerPath", back_populates="skills")
    user_skills: Mapped[list["UserSkill"]] = relationship(
        "UserSkill", back_populates="skill", cascade="all, delete-orphan"
    )


class UserSkill(UUIDMixin, TimestampMixin, Base):
    """Association between a user and a skill, with a 0-100 progress level."""
    __tablename__ = "user_skills"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    skill_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    # Progress from 0 (beginner) to 100 (mastered)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="user_skills")  # type: ignore[name-defined]
    skill: Mapped["Skill"] = relationship("Skill", back_populates="user_skills")
