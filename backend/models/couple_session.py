from datetime import datetime
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class CoupleSession(Base):
    __tablename__ = "couple_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    male_name: Mapped[str] = mapped_column(String, nullable=False)
    female_name: Mapped[str] = mapped_column(String, nullable=False)

    status: Mapped[str] = mapped_column(String, default="in_progress", nullable=False)

    male_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    female_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # timestamp mulai & selesai
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
