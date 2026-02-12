
# Import all models for Alembic
from app.models.base import Base
from app.models.account import User
from app.models.session import Session
from app.models.question import Question
from app.models.practice_test import PracticeTest
from app.models.submission import Submission
from app.models.result import GradingResult
from app.models.suggestion import LearningSuggestion
from app.models.history import LearningHistory
