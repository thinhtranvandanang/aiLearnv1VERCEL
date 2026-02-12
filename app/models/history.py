from sqlalchemy import Integer, ForeignKey, Float, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class LearningHistory(Base):
    __tablename__ = "learning_history"
    
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    total_tests_taken: Mapped[int] = mapped_column(Integer, default=0)
    average_score: Mapped[float] = mapped_column(Float, default=0.0)
    progress_trend: Mapped[str | None] = mapped_column(String) # simple descriptive string
