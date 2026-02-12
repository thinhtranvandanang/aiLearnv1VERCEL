from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from app.models.question import test_question_association

class PracticeTest(Base):
    __tablename__ = "practice_tests"
    
    title: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    duration_minutes: Mapped[int] = mapped_column(Integer, default=45)
    status: Mapped[str] = mapped_column(String, default="ready") # ready, completed

    student: Mapped["User"] = relationship("User", back_populates="practice_tests")
    questions: Mapped[list["Question"]] = relationship(
        "Question", 
        secondary=test_question_association, 
        back_populates="practice_tests"
    )
    submissions: Mapped[list["Submission"]] = relationship("Submission", back_populates="practice_test")
