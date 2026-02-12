from datetime import datetime
from sqlalchemy import String, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class Submission(Base):
    __tablename__ = "submissions"
    
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    test_id: Mapped[int] = mapped_column(ForeignKey("practice_tests.id"))
    type: Mapped[str] = mapped_column(String, nullable=False) # online, offline
    file_path: Mapped[str | None] = mapped_column(String) # For offline images
    answers: Mapped[str | None] = mapped_column(Text) # JSON mapping
    status: Mapped[str] = mapped_column(String, default="pending") # pending, graded
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime)

    student: Mapped["User"] = relationship("User", back_populates="submissions")
    practice_test: Mapped["PracticeTest"] = relationship("PracticeTest", back_populates="submissions")
    result: Mapped["GradingResult"] = relationship("GradingResult", back_populates="submission", uselist=False)
