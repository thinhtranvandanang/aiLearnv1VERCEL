
from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: Optional[str] = None
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Any = None, message: str = "Operation successful"):
        return cls(status="success", message=message, data=data)

    @classmethod
    def error(cls, message: str = "An error occurred", status: str = "error"):
        return cls(status=status, message=message, data=None)
