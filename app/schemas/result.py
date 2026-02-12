
from typing import List, Dict, Any
from pydantic import BaseModel

class QuestionFeedback(BaseModel):
    question_id: int
    student_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str

class ResultOut(BaseModel):
    submission_id: int
    score: float
    total_questions: int
    correct_answers: int
    wrong_answers: int
    feedback: List[QuestionFeedback]

class LearningSuggestionOut(BaseModel):
    topic: str
    priority: int
    content: str

class HistorySummary(BaseModel):
    total_tests: int
    average_score: float
    progress_trend: str
    recent_tests: List[Dict[str, Any]]
