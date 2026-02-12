
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.submission import OnlineSubmissionRequest
from app.services.submission_service import submission_service
from app.core.response import APIResponse
from app.models.account import User

router = APIRouter()

@router.post("/{testId}/submit-online")
def submit_online(
    testId: int,
    request: OnlineSubmissionRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Nộp bài làm trực tuyến."""
    submission = submission_service.submit_online(
        db, current_user.id, testId, request.answers, request.start_time, request.end_time
    )
    return APIResponse.success(data={"submission_id": submission.id})

@router.post("/{testId}/submit-offline")
async def submit_offline(
    testId: int,
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Nộp bài làm ngoại tuyến qua file/ảnh."""
    # Logic lưu file thực tế ở đây
    file_path = f"uploads/{file.filename}"
    submission = submission_service.submit_offline(db, current_user.id, testId, file_path)
    return APIResponse.success(data={"submission_id": submission.id})
