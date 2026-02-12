
import random
from sqlalchemy.orm import Session
from app.models.question import Question
from app.models.practice_test import PracticeTest
from app.models.account import User
from app.core.exceptions import BusinessLogicException, NotFoundException

class PracticeTestService:
    @staticmethod
    def generate_test(db: Session, student_id: int, subject: str, topic: str, level: str, count: int):
        # 1. Tìm câu hỏi phù hợp
        questions = db.query(Question).filter(
            Question.subject == subject,
            Question.topic == topic,
            Question.level == level
        ).all()
        
        if len(questions) < count:
            raise BusinessLogicException(f"Không đủ câu hỏi theo tiêu chí yêu cầu. Hiện có: {len(questions)}")
        
        selected_questions = random.sample(questions, count)
        
        # 2. Tạo đề
        test = PracticeTest(
            title=f"Đề luyện tập {subject} - {topic}",
            subject=subject,
            student_id=student_id,
            duration_minutes=count * 2, # Giả định 2p/câu
            status="ready"
        )
        test.questions = selected_questions
        
        db.add(test)
        db.commit()
        db.refresh(test)
        return test

    @staticmethod
    def get_test_content(db: Session, test_id: int, student_id: int):
        test = db.query(PracticeTest).filter(PracticeTest.id == test_id).first()
        if not test:
            raise NotFoundException("Đề luyện tập")
        if test.student_id != student_id:
            raise BusinessLogicException("Bạn không có quyền truy cập đề này")
        
        # Build response manually to avoid serialization issues
        questions_data = []
        for question in test.questions:
            questions_data.append({
                "id": question.id,
                "content": question.content,
                "options": question.options
            })
        
        return {
            "id": test.id,
            "title": test.title,
            "subject": test.subject,
            "question_count": len(test.questions),
            "duration_minutes": test.duration_minutes,
            "status": test.status,
            "questions": questions_data
        }

    @staticmethod
    def export_test(db: Session, test_id: int, student_id: int, format: str):
        # Giả lập logic sinh file PDF/DOCX
        return {"filename": f"test_{test_id}.{format}", "url": f"/downloads/test_{test_id}"}

test_service = PracticeTestService()
