
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class OnlineSubmissionRequest(BaseModel):
    answers: Dict[int, str] # question_id -> student_answer
    start_time: datetime
    end_time: datetime

class SubmissionResponse(BaseModel):
    id: int
    status: str
    submitted_at: datetime
    message: str = "Submission received successfully"

    class Config:
        from_attributes = True
