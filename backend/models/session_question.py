from sqlalchemy import Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class SessionQuestion(Base):
    """
    Menyimpan 5 soal yang dipilih untuk setiap player agar konsisten
    (cowok dapat set soal tetap, cewek dapat set soal tetap).
    """
    __tablename__ = "session_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    couple_session_id: Mapped[int] = mapped_column(ForeignKey("couple_sessions.id"), nullable=False)
    player: Mapped[str] = mapped_column(String, nullable=False)  # "male" or "female"
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)  # 1..5

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("couple_session_id", "player", "order_index", name="uq_session_player_order"),
    )
