import httpx
import secrets
import logging
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token, get_password_hash
from app.models.account import User
from app.core.exceptions import AuthException

logger = logging.getLogger(__name__)

class GoogleAuthService:
    @staticmethod
    def get_google_auth_url() -> str:
        """Tạo URL để người dùng đăng nhập qua Google OAuth 2.0."""
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account"
        }
        query_params = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_params}"

    @staticmethod
    async def verify_and_login(db: Session, code: str) -> str:
        """
        Trao đổi authorization code lấy access_token, 
        xác thực profile và trả về hệ thống JWT token.
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                # 1. Trao đổi Authorization Code lấy Tokens
                token_url = "https://oauth2.googleapis.com/token"
                data = {
                    "code": code,
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",
                }
                
                token_response = await client.post(token_url, data=data)
                token_data = token_response.json()
                
                if token_response.status_code != 200:
                    logger.error(f"Google Token Exchange Error: {token_data}")
                    raise AuthException(f"Google Auth Error: {token_data.get('error_description', 'Invalid Code')}")

                access_token = token_data.get("access_token")

                # 2. Lấy thông tin người dùng từ Google UserInfo API
                user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
                user_info_response = await client.get(
                    user_info_url, 
                    headers={"Authorization": f"Bearer {access_token}"}
                )
                google_user = user_info_response.json()

                if user_info_response.status_code != 200:
                    logger.error(f"Google UserInfo Error: {google_user}")
                    raise AuthException("Không thể lấy dữ liệu profile từ Google")

                email = google_user.get("email")
                full_name = google_user.get("name") or google_user.get("given_name") or email.split('@')[0]

                if not email:
                    raise AuthException("Email không được cung cấp từ Google account")

                # 3. Xử lý đồng bộ User trong hệ thống
                user = db.query(User).filter(User.email == email).first()
                
                if not user:
                    # Tự động tạo tài khoản mới nếu email chưa tồn tại
                    username = f"{email.split('@')[0]}_{secrets.token_hex(2)}"
                    
                    user = User(
                        username=username,
                        email=email,
                        full_name=full_name,
                        hashed_password=get_password_hash(secrets.token_urlsafe(32)),
                        role="student",
                        is_active=True
                    )
                    try:
                        db.add(user)
                        db.commit()
                        db.refresh(user)
                        logger.info(f"Created new user via Google: {email}")
                    except Exception as db_err:
                        db.rollback()
                        logger.error(f"Database error during Google user creation: {db_err}")
                        raise AuthException("Lỗi hệ thống khi tạo tài khoản")

                if not user.is_active:
                    raise AuthException("Tài khoản của bạn hiện đang bị khóa")

                # 4. Trả về JWT token của hệ thống EduNexia
                return create_access_token(subject=user.id)

            except httpx.RequestError as exc:
                logger.error(f"HTTP Request error while talking to Google: {exc}")
                raise AuthException("Lỗi kết nối tới máy chủ Google")
            except Exception as e:
                logger.error(f"Unexpected error in verify_and_login: {e}")
                if 'db' in locals():
                    db.rollback()
                raise e

google_auth_service = GoogleAuthService()