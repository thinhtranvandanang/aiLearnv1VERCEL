from sqlalchemy import Integer, ForeignKey, Text, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

class LearningSuggestion(Base):
    __tablename__ = "learning_suggestions"
    
    result_id: Mapped[int] = mapped_column(ForeignKey("grading_results.id"))
    topic: Mapped[str] = mapped_column(String, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, default=1) # 1: high, 2: medium, 3: low
    content: Mapped[str] = mapped_column(Text, nullable=False)

    result: Mapped["GradingResult"] = relationship("GradingResult", back_populates="suggestions")
