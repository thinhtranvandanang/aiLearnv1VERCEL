from sqlalchemy import Float, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class GradingResult(Base):
    __tablename__ = "grading_results"
    
    submission_id: Mapped[int] = mapped_column(ForeignKey("submissions.id"))
    score: Mapped[float] = mapped_column(Float, nullable=False)
    total_questions: Mapped[int] = mapped_column(Integer, nullable=False)
    correct_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    wrong_answers: Mapped[int] = mapped_column(Integer, nullable=False)
    feedback_details: Mapped[str | None] = mapped_column(Text) # JSON string

    submission: Mapped["Submission"] = relationship("Submission", back_populates="result")
    suggestions: Mapped[list["LearningSuggestion"]] = relationship("LearningSuggestion", back_populates="result")
