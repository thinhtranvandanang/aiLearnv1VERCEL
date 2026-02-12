from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

# Sử dụng bcrypt làm scheme chính. 
# Lưu ý: bcrypt có giới hạn cứng là 72 ký tự cho mật khẩu đầu vào.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Cắt tỉa password về 72 ký tự để tương thích với giới hạn của bcrypt
    safe_password = plain_password[:72] if plain_password else ""
    return pwd_context.verify(safe_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Cắt tỉa password về 72 ký tự trước khi hash để tránh ValueError
    safe_password = password[:72] if password else ""
    return pwd_context.hash(safe_password)