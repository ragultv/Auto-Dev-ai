import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:ragul%402004@localhost:5432/autodev")

# For SQLite (development)
# DATABASE_URL = "sqlite:///./aiml_pipeline.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Create all tables in the database"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database"""
    create_tables()
    print("Database tables created successfully!")
