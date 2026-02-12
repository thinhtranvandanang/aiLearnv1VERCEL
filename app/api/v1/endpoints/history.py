
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.services.history_service import history_service
from app.core.response import APIResponse
from app.models.account import User

router = APIRouter()

@router.get("/me/learning-history")
def get_history(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Xem tổng hợp lịch sử học tập."""
    history = history_service.get_history(db, current_user.id)
    return APIResponse.success(data=history)

@router.get("/me/learning-history/{submissionId}")
def get_detail(
    submissionId: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Xem chi tiết một bài đã làm trong quá khứ."""
    from app.services.grading_service import grading_service
    result = grading_service.get_result(db, submissionId, current_user.id)
    return APIResponse.success(data=result)
