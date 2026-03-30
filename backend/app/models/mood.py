"""
app/models/mood.py
──────────────────
Daily mood-tracking log for the Stress & Overthinking module.
"""
from __future__ import annotations

import uuid
from typing import Optional, TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User


class MoodLog(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "mood_logs"

    # Rating: 1 (very bad) – 10 (excellent)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    log_date: Mapped[str] = mapped_column(Date, nullable=False)  # YYYY-MM-DD

    # ── FK ─────────────────────────────────────────────────────────────────────
    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    owner: Mapped["User"] = relationship("User", back_populates="mood_logs")

    def __repr__(self) -> str:
        return f"<MoodLog id={self.id} rating={self.rating} date={self.log_date}>"
