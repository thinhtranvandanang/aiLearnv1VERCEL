from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import Integer, DateTime

class Base(DeclarativeBase):
    """
    Base class chuẩn cho SQLAlchemy 2.0.
    Sử dụng Mapped và mapped_column để giải quyết triệt để lỗi 
    'Type annotation for User.id can't be correctly interpreted'.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
