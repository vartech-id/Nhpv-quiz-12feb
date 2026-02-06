from pydantic import BaseModel, Field


class CoupleSessionCreate(BaseModel):
    male_name: str = Field(min_length=1, max_length=64)
    female_name: str = Field(min_length=1, max_length=64)


class CoupleSessionCreated(BaseModel):
    id: int
    current_player: str  # "male"


class AnswerItem(BaseModel):
    question_id: int
    answer: str  # "A" or "B"


class SubmitAnswers(BaseModel):
    player: str  # "male" or "female"
    answers: list[AnswerItem]


class SubmitMaleResponse(BaseModel):
    player: str
    score: int
    next_player: str  # "female"


class SubmitFinalResponse(BaseModel):
    male_score: int
    female_score: int
    status: str  # "done"
