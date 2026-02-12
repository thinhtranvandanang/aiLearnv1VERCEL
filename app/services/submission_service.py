
import json
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.practice_test import PracticeTest
from app.core.exceptions import BusinessLogicException, NotFoundException

class SubmissionService:
    @staticmethod
    def submit_online(db: Session, student_id: int, test_id: int, answers: dict, start_time: datetime, end_time: datetime):
        test = db.query(PracticeTest).filter(PracticeTest.id == test_id).first()
        if not test:
            raise NotFoundException("Đề luyện tập")
        if test.student_id != student_id:
            raise BusinessLogicException("Bạn không có quyền nộp bài cho đề này")
        
        # Kiểm tra xem đã nộp chưa
        existing = db.query(Submission).filter(Submission.test_id == test_id).first()
        if existing:
            raise BusinessLogicException("Bài đã được nộp trước đó")

        submission = Submission(
            student_id=student_id,
            test_id=test_id,
            type="online",
            answers=json.dumps({str(k): v for k, v in answers.items()}),
            status="graded", # Chấm online luôn
            submitted_at=end_time
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        
        # Gọi grading_service (giả định được import hoặc inject)
        from app.services.grading_service import grading_service
        grading_service.grade_submission(db, submission.id)
        
        return submission

    @staticmethod
    def submit_offline(db: Session, student_id: int, test_id: int, file_path: str):
        test = db.query(PracticeTest).filter(PracticeTest.id == test_id).first()
        if not test:
            raise NotFoundException("Đề luyện tập")
        
        submission = Submission(
            student_id=student_id,
            test_id=test_id,
            type="offline",
            file_path=file_path,
            status="pending",
            submitted_at=datetime.utcnow()
        )
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return submission

submission_service = SubmissionService()
