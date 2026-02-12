
from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.test import TestGenerateRequest, TestContent
from app.services.test_service import test_service
from app.core.response import APIResponse
from app.models.account import User

router = APIRouter()

@router.post("/generate")
def generate(
    request: TestGenerateRequest, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Tạo đề luyện tập mới dựa trên tiêu chí."""
    # Debug logging
    print(f"🔍 DEBUG: Generate test request - User: {current_user.id}, Subject: {request.subject}, Topic: {request.topic}, Level: {request.level}, Count: {request.question_count}")
    
    test = test_service.generate_test(
        db, current_user.id, request.subject, request.topic, request.level, request.question_count
    )
    return APIResponse.success(data={"test_id": test.id, "title": test.title})

@router.get("/{testId}/content")
def get_content(
    testId: int, 
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Tải nội dung đề cho học sinh."""
    test = test_service.get_test_content(db, testId, current_user.id)
    return APIResponse.success(data=test)

@router.get("/{testId}/download")
def download(
    testId: int,
    format: str = "pdf",
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_student)
):
    """Xuất đề ra file."""
    result = test_service.export_test(db, testId, current_user.id, format)
    return APIResponse.success(data=result)
