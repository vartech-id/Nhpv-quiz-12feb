from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class PlayerResult(Base):
    __tablename__ = "player_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    couple_session_id: Mapped[int] = mapped_column(ForeignKey("couple_sessions.id"), nullable=False)
    player: Mapped[str] = mapped_column(String, nullable=False)  # "male" or "female"
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..5

    __table_args__ = (
        UniqueConstraint("couple_session_id", "player", name="uq_session_player_result"),
    )
