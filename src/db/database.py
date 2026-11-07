from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.settings import settings

database_url = (
    settings.TEST_DATABASE_URL
    if settings.ENV == "test" and settings.TEST_DATABASE_URL
    else settings.DATABASE_URL
)

engine = create_engine(
    database_url,
    echo=True,
    pool_size=20,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
