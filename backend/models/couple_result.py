from datetime import datetime
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class CoupleResult(Base):
    __tablename__ = "couple_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    couple_session_id: Mapped[int] = mapped_column(
        ForeignKey("couple_sessions.id"),
        unique=True,
        index=True,
        nullable=False,
    )

    # snapshot untuk report
    male_name: Mapped[str] = mapped_column(String, nullable=False)
    female_name: Mapped[str] = mapped_column(String, nullable=False)

    male_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    female_score: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    total_players: Mapped[int] = mapped_column(Integer, nullable=False, default=2)

    # timestamp (copy dari session)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
