"""
Worker schemas module
Handles Pydantic schemas for worker data validation
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class WorkerBase(BaseModel):
    """Base worker schema with common fields"""
    first_name: str
    last_name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = 0
    bio: Optional[str] = None
    hourly_rate: Optional[int] = None  # Rate in cents
    availability: Optional[Dict[str, Any]] = None

class WorkerCreate(WorkerBase):
    """Schema for creating a new worker"""
    user_id: int

class WorkerUpdate(BaseModel):
    """Schema for updating worker data"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    bio: Optional[str] = None
    hourly_rate: Optional[int] = None
    availability: Optional[Dict[str, Any]] = None

class WorkerResponse(WorkerBase):
    """Schema for worker response data"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 