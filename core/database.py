"""
Database configuration module
Handles database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database configuration
DATABASE_URL = "mysql+mysqlconnector://root:Parth%402000@localhost/workshift"

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=30,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

def get_db():
    """
    Database dependency for FastAPI
    Yields a database session and ensures it's closed
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 