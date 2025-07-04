from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
# Import all models so SQLAlchemy knows about them
from models.user import User
from models.business_owner import BusinessOwner
from models.worker import Worker
from models.job import Job
from models.job_application import JobApplication
from api import user_routes, business_owner_routes, worker_routes, job_routes, application_routes
from api.auth import router as auth_router
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

app = FastAPI()

origins = [
    "https://34.123.43.254",  # New frontend IP
    "http://localhost:3000",  # Local development
    "http://127.0.0.1:3000"   # Local development (alternative)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Remove Base.metadata.create_all for Alembic migrations
# Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def check_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful.")
    except SQLAlchemyError as e:
        print("Database connection failed:", e)
        raise e  # This will stop the app if DB is not reachable

app.include_router(user_routes.router)
app.include_router(business_owner_routes.router)
app.include_router(worker_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"]) 