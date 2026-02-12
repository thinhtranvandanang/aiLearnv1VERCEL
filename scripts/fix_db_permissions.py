import sys
import os
from sqlalchemy import create_engine, text

# Thêm thư mục gốc vào path để import settings
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

def fix_permissions():
    """
    Tự động cấp quyền GRANT ALL ON SCHEMA public cho user đang cấu hình trong .env
    Dành cho PostgreSQL 15+ nơi quyền public bị hạn chế mặc định.
    """
    print(f"Connecting to: {settings.DATABASE_URL}")
    engine = create_engine(settings.DATABASE_URL)
    
    # Trích xuất username từ DATABASE_URL
    # URL format: postgresql://user:pass@host:port/db
    try:
        db_user = settings.DATABASE_URL.split('://')[1].split(':')[0]
    except Exception:
        print("Could not parse DB user from URL. Please run SQL manually.")
        return

    sql = text(f'GRANT ALL ON SCHEMA public TO "{db_user}";')
    
    try:
        with engine.connect() as conn:
            conn.execute(sql)
            conn.commit()
            print(f"Successfully granted ALL permissions on schema 'public' to user '{db_user}'.")
            print("You can now run: alembic revision --autogenerate -m 'Initial schema'")
    except Exception as e:
        print(f"Error: {e}")
        print("\nNote: You might need to run this as a superuser (postgres) if your user lacks GRANT privileges.")

if __name__ == "__main__":
    fix_permissions()
