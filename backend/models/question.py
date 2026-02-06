from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Contoh: '"Aku Kangen" Artinya...'
    question_text: Mapped[str] = mapped_column(String, nullable=False)

    # Teks pilihan
    option_a: Mapped[str] = mapped_column(String, nullable=False)
    option_b: Mapped[str] = mapped_column(String, nullable=False)

    # "A" atau "B"
    correct_answer: Mapped[str] = mapped_column(String(1), nullable=False)

    # "male" atau "female"
    target: Mapped[str] = mapped_column(String, nullable=False)
