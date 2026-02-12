
from fastapi import HTTPException, status

class EduNexiaException(HTTPException):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        super().__init__(status_code=status_code, detail=detail)

class AuthException(EduNexiaException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail=detail, status_code=status.HTTP_401_UNAUTHORIZED)

class NotFoundException(EduNexiaException):
    def __init__(self, item: str = "Item"):
        super().__init__(detail=f"{item} not found", status_code=status.HTTP_404_NOT_FOUND)

class PermissionException(EduNexiaException):
    def __init__(self, detail: str = "Permission denied"):
        super().__init__(detail=detail, status_code=status.HTTP_403_FORBIDDEN)

class BusinessLogicException(EduNexiaException):
    def __init__(self, detail: str):
        super().__init__(detail=detail, status_code=status.HTTP_400_BAD_REQUEST)
