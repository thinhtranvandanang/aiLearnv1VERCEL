
import json
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.result import GradingResult
from app.models.practice_test import PracticeTest
from app.core.exceptions import NotFoundException, BusinessLogicException

class GradingService:
    @staticmethod
    def grade_submission(db: Session, submission_id: int):
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise NotFoundException("Bài làm")
        
        if submission.status == "pending" and submission.type == "offline":
            # Trong thực tế sẽ gọi AI OCR ở đây
            pass

        # Lấy đáp án chuẩn từ đề
        test = submission.practice_test
        student_answers = json.loads(submission.answers) if submission.answers else {}
        
        correct_count = 0
        feedback = []
        
        for q in test.questions:
            ans = student_answers.get(str(q.id))
            is_correct = ans == q.correct_answer
            if is_correct:
                correct_count += 1
            feedback.append({
                "question_id": q.id,
                "student_answer": ans,
                "correct_answer": q.correct_answer,
                "is_correct": is_correct,
                "explanation": q.explanation
            })
            
        total = len(test.questions)
        score = (correct_count / total) * 10 if total > 0 else 0
        
        result = GradingResult(
            submission_id=submission_id,
            score=round(score, 2),
            total_questions=total,
            correct_answers=correct_count,
            wrong_answers=total - correct_count,
            feedback_details=json.dumps(feedback)
        )
        
        submission.status = "graded"
        db.add(result)
        db.commit()
        return result

    @staticmethod
    def get_result(db: Session, submission_id: int, student_id: int):
        submission = db.query(Submission).filter(Submission.id == submission_id).first()
        if not submission:
            raise NotFoundException("Bài làm")
        if submission.student_id != student_id:
            raise BusinessLogicException("Bạn không có quyền xem bài này")
        if submission.status != "graded":
            raise BusinessLogicException("Bài chưa được chấm")
        
        result = submission.result
        if not result:
            raise BusinessLogicException("Không tìm thấy kết quả")
        
        # Build response manually to avoid serialization issues
        return {
            "id": result.id,
            "submission_id": result.submission_id,
            "score": result.score,
            "total_questions": result.total_questions,
            "correct_answers": result.correct_answers,
            "wrong_answers": result.wrong_answers,
            "feedback_details": result.feedback_details
        }

grading_service = GradingService()
