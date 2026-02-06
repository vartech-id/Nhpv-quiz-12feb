from pydantic import BaseModel


class QuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    correct_answer: str  # "A" or "B" (buat animasi FE)


class QuestionsResponse(BaseModel):
    questions: list[QuestionOut]
