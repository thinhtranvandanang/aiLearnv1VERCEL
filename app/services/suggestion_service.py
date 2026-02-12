
import json
from sqlalchemy.orm import Session
from app.models.result import GradingResult
from app.models.suggestion import LearningSuggestion
from app.core.exceptions import BusinessLogicException

class SuggestionService:
    @staticmethod
    def get_suggestions(db: Session, submission_id: int, student_id: int):
        result = db.query(GradingResult).filter(GradingResult.submission_id == submission_id).first()
        if not result:
            raise BusinessLogicException("Bài chưa được chấm nên chưa có gợi ý")
        
        if result.submission.student_id != student_id:
            raise BusinessLogicException("Permission denied")

        # Phân tích logic
        feedback = json.loads(result.feedback_details)
        wrong_questions = [f for f in feedback if not f['is_correct']]
        
        if not wrong_questions:
            return [{
                "topic": "General", 
                "priority": 3, 
                "content": "Tuyệt vời! Bạn đã làm đúng hết. Hãy thử thách với độ khó cao hơn."
            }]

        # Mô phỏng gợi ý
        suggestions = [
            {
                "topic": "Kiến thức hổng", 
                "priority": 1, 
                "content": f"Bạn sai {len(wrong_questions)} câu. Cần ôn lại các khái niệm cơ bản về chương này."
            }
        ]
        return suggestions

suggestion_service = SuggestionService()
