"""
Job Application schemas module
Handles Pydantic schemas for job application data validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.job_application import ApplicationStatus

class JobApplicationBase(BaseModel):
    """Base job application schema with common fields"""
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: Optional[ApplicationStatus] = ApplicationStatus.PENDING

class JobApplicationCreate(JobApplicationBase):
    """Schema for creating a new job application"""
    job_id: int
    worker_id: int

class JobApplicationUpdate(BaseModel):
    """Schema for updating job application data"""
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: Optional[ApplicationStatus] = None

class JobApplicationResponse(JobApplicationBase):
    """Schema for job application response data"""
    id: int
    job_id: int
    worker_id: int
    applied_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 