from sqlalchemy.orm import Session
from app.core.database import SessionLocal


def get_db():
    """
    Database session dependency for FastAPI.
    Ensures session is properly closed after request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
