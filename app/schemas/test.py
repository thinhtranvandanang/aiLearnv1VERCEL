
from typing import List, Optional
from pydantic import BaseModel

class TestGenerateRequest(BaseModel):
    subject: str
    topic: str
    level: str
    question_count: Optional[int] = 1

class TestSummary(BaseModel):
    id: int
    title: str
    subject: str
    question_count: int
    duration_minutes: int
    status: str

    class Config:
        from_attributes = True

class QuestionOut(BaseModel):
    id: int
    content: str
    options: Optional[str] = None # JSON string or actual dict if parsed

    class Config:
        from_attributes = True

class TestContent(TestSummary):
    questions: List[QuestionOut]
