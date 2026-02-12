import secrets
import logging
import re
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.account import User
from app.core.security import verify_password, create_access_token, get_password_hash
from app.core.exceptions import AuthException, BusinessLogicException
from app.schemas.auth import UserCreate

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def authenticate_student(db: Session, username: str, password: str):
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise AuthException("Tài khoản không tồn tại")
        
        if not verify_password(password, user.hashed_password):
            raise AuthException("Thông tin đăng nhập không đúng")
        
        if not user.is_active:
            raise AuthException("Tài khoản bị khóa")
        
        token = create_access_token(subject=user.id)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_active": user.is_active
            }
        }

    @staticmethod
    def register_student(db: Session, user_in: UserCreate):
        if db.query(User).filter(User.username == user_in.username).first():
            raise BusinessLogicException("Tên đăng nhập đã tồn tại")
        if db.query(User).filter(User.email == user_in.email).first():
            raise BusinessLogicException("Email đã được sử dụng")

        user = User(
            username=user_in.username,
            email=user_in.email,
            full_name=user_in.full_name,
            hashed_password=get_password_hash(user_in.password),
            role="student",
            is_active=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        token = create_access_token(subject=user.id)
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_active": user.is_active
            }
        }

    @staticmethod
    def get_or_create_google_user(db: Session, email: str, full_name: str, google_id: str) -> User:
        """
        Tìm hoặc tạo user từ Google. Chuẩn hóa email lowercase.
        Xử lý IntegrityError triệt để nếu có tranh chấp tạo user đồng thời.
        """
        email = (email or "").strip().lower()
        if not email:
            raise AuthException("Email không hợp lệ từ Google")

        # 1. Tìm theo email trước
        user = db.query(User).filter(User.email == email).first()
        if user:
            return user

        # 2. Tạo username an toàn từ email
        base_username = email.split('@')[0]
        username = re.sub(r'[^a-zA-Z0-9_]', '', base_username).lower()
        if not username:
            username = f"u_{secrets.token_hex(4)}"

        # Kiểm tra trùng username, nếu trùng thì thêm hậu tố ngẫu nhiên
        original_username = username
        while db.query(User).filter(User.username == username).first():
            username = f"{original_username}_{secrets.token_hex(2)}"

        try:
            # Dùng secrets.token_hex(16) tạo mật khẩu ngẫu nhiên 32 ký tự.
            # Rất an toàn và nằm gọn trong giới hạn 72 ký tự của bcrypt.
            random_password = secrets.token_hex(16)
            
            user = User(
                username=username,
                email=email,
                full_name=full_name or base_username,
                hashed_password=get_password_hash(random_password),
                role="student",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Successfully created Google user: {email}")
            return user
        except IntegrityError:
            db.rollback()
            # Thử tìm lại lần cuối đề phòng race condition
            user = db.query(User).filter(User.email == email).first()
            if user:
                return user
            raise AuthException("Không thể đồng bộ tài khoản Google")

auth_service = AuthService()