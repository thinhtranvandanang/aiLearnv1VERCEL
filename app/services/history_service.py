
from sqlalchemy.orm import Session
from app.models.submission import Submission
from app.models.result import GradingResult

class HistoryService:
    @staticmethod
    def get_history(db: Session, student_id: int):
        submissions = db.query(Submission).filter(Submission.student_id == student_id).all()
        
        results = []
        total_score = 0
        count = 0
        
        for sub in submissions:
            if sub.result:
                results.append({
                    "id": sub.id,
                    "test_title": sub.practice_test.title,
                    "score": sub.result.score,
                    "submitted_at": sub.submitted_at
                })
                total_score += sub.result.score
                count += 1
        
        avg = total_score / count if count > 0 else 0
        
        return {
            "total_tests": len(submissions),
            "average_score": round(avg, 2),
            "progress_trend": "Ổn định" if avg >= 5 else "Cần cố gắng",
            "recent_tests": results[-5:] # Lấy 5 bài gần nhất
        }

history_service = HistoryService()
