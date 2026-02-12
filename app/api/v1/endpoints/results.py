
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services.grading_service import grading_service
from app.services.suggestion_service import suggestion_service
from app.core.response import APIResponse
from app.models.account import User

router = APIRouter()

@router.get("/{submissionId}/result")
def get_result(
    submissionId: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Xem kết quả chấm bài chi tiết."""
    result = grading_service.get_result(db, submissionId, current_user.id)
    return APIResponse.success(data=result)

@router.get("/{submissionId}/learning-suggestions")
def get_suggestions(
    submissionId: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Nhận gợi ý học tập sau khi làm bài."""
    suggestions = suggestion_service.get_suggestions(db, submissionId, current_user.id)
    return APIResponse.success(data=suggestions)
