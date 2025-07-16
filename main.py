from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from core.database import engine, Base
# Import all models so SQLAlchemy knows about them
from models.user import User
from models.business_owner import BusinessOwner
from models.worker import Worker
from models.job import Job
from models.job_application import JobApplication
from api import user_routes, business_owner_routes, worker_routes, job_routes, application_routes, notification_routes
from api.auth import router as auth_router
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import text
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

# Global exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.warning(f"Validation error: {exc.errors()}")
    
    # Convert errors to serializable format
    serializable_errors = []
    for error in exc.errors():
        serializable_error = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
            "input": str(error.get("input", ""))  # Convert input to string
        }
        # Handle the ctx field which might contain non-serializable objects
        if "ctx" in error:
            ctx = error["ctx"]
            serializable_ctx = {}
            for key, value in ctx.items():
                if isinstance(value, (str, int, float, bool, type(None))):
                    serializable_ctx[key] = value
                elif isinstance(value, Exception):
                    # Handle Exception objects (like ValueError) by converting to string
                    serializable_ctx[key] = str(value)
                else:
                    serializable_ctx[key] = str(value)  # Convert to string
            serializable_error["ctx"] = serializable_ctx
        
        serializable_errors.append(serializable_error)
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": serializable_errors
        }
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """Handle Pydantic model validation errors"""
    logger.warning(f"Pydantic validation error: {exc.errors()}")
    
    # Convert errors to serializable format
    serializable_errors = []
    for error in exc.errors():
        serializable_error = {
            "type": error["type"],
            "loc": error["loc"],
            "msg": error["msg"],
            "input": str(error.get("input", ""))  # Convert input to string
        }
        # Handle the ctx field which might contain non-serializable objects
        if "ctx" in error:
            ctx = error["ctx"]
            serializable_ctx = {}
            for key, value in ctx.items():
                if isinstance(value, (str, int, float, bool, type(None))):
                    serializable_ctx[key] = value
                elif isinstance(value, Exception):
                    # Handle Exception objects (like ValueError) by converting to string
                    serializable_ctx[key] = str(value)
                else:
                    serializable_ctx[key] = str(value)  # Convert to string
            serializable_error["ctx"] = serializable_ctx
        
        serializable_errors.append(serializable_error)
    
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": serializable_errors
        }
    )

@app.exception_handler(IntegrityError)
async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors"""
    logger.error(f"Database integrity error: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Database integrity error",
            "message": "The data violates database constraints"
        }
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Database error",
            "message": "An error occurred while accessing the database"
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": "An unexpected error occurred"
        }
    )

app.include_router(user_routes.router)
app.include_router(business_owner_routes.router)
app.include_router(worker_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router) 
app.include_router(notification_routes.router)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"]) 