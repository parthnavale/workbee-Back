import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load the database URL from environment variable
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "WORKBEE_DATABASE_URL",
    "mysql+mysqlconnector://root:Parth%402000@localhost:3306/workbee_db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 