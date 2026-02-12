from typing import List, Union, Optional
from pydantic import AnyHttpUrl, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "EduNexia API"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "development_secret_key_change_me_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/edunexia"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []
    ALLOWED_ORIGINS: Optional[str] = None

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            # Tách chuỗi bằng dấu phẩy và loại bỏ khoảng trắng + dấu / ở cuối
            return [i.strip().rstrip("/") for i in v.split(",") if i.strip()]
        elif isinstance(v, list):
            return [str(i).strip().rstrip("/") for i in v]
        return []
    
    @model_validator(mode="after")
    def sync_cors_origins(self) -> "Settings":
        """Nếu có ALLOWED_ORIGINS trong .env, nạp vào BACKEND_CORS_ORIGINS."""
        if self.ALLOWED_ORIGINS and not self.BACKEND_CORS_ORIGINS:
            origins = [i.strip().rstrip("/") for i in self.ALLOWED_ORIGINS.split(",") if i.strip()]
            self.BACKEND_CORS_ORIGINS = origins
        return self

    # Google OAuth / Frontend
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None
    GOOGLE_REDIRECT_URI: Optional[str] = None
    FRONTEND_URL: str = "http://localhost:3000"

    # File Storage
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_FILE_EXTENSIONS: List[str] = ["jpg", "jpeg", "png", "pdf"]

    model_config = SettingsConfigDict(
        case_sensitive=True, 
        env_file=".env",
        extra="ignore"
    )

settings = Settings()