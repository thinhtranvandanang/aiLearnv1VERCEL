from sqlalchemy import String, Text, Integer, Table, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

# Định nghĩa bảng trung gian (Association Table) chuẩn cho SQLAlchemy 2.0
test_question_association = Table(
    "test_question_association",
    Base.metadata,
    Column("test_id", Integer, ForeignKey("practice_tests.id"), primary_key=True),
    Column("question_id", Integer, ForeignKey("questions.id"), primary_key=True)
)

class Question(Base):
    __tablename__ = "questions"
    
    subject: Mapped[str] = mapped_column(String, index=True, nullable=False)
    topic: Mapped[str] = mapped_column(String, index=True, nullable=False)
    level: Mapped[str] = mapped_column(String, index=True, nullable=False) # easy, medium, hard
    content: Mapped[str] = mapped_column(Text, nullable=False)
    options: Mapped[str | None] = mapped_column(Text) # JSON string of choices
    correct_answer: Mapped[str] = mapped_column(String, nullable=False)
    explanation: Mapped[str | None] = mapped_column(Text)

    practice_tests: Mapped[list["PracticeTest"]] = relationship(
        "PracticeTest", 
        secondary=test_question_association, 
        back_populates="questions"
    )
