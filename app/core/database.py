from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Import all models so that SQLAlchemy can resolve relationship() 
# string references like "Session" when mappers are configured.
# This import is required for proper mapper configuration at application startup.
from app.db import base  # noqa: F401

# Engine setup
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)