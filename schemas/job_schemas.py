"""
Job schemas module
Handles Pydantic schemas for job data validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.job import JobStatus

class JobBase(BaseModel):
    """Base job schema with common fields"""
    title: str
    description: str
    requirements: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[int] = None  # Salary in cents
    salary_max: Optional[int] = None  # Salary in cents
    hourly_rate: Optional[int] = None  # Hourly rate in cents
    duration: Optional[str] = None
    skills_required: Optional[List[str]] = None
    status: Optional[JobStatus] = JobStatus.ACTIVE

class JobCreate(JobBase):
    """Schema for creating a new job"""
    business_owner_id: int

class JobUpdate(BaseModel):
    """Schema for updating job data"""
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    hourly_rate: Optional[int] = None
    duration: Optional[str] = None
    skills_required: Optional[List[str]] = None
    status: Optional[JobStatus] = None

class JobResponse(JobBase):
    """Schema for job response data"""
    id: int
    business_owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 