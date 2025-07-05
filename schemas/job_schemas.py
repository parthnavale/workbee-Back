from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
import re

class JobCreate(BaseModel):
    business_owner_id: int
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    hourly_rate: Optional[float] = None
    estimated_hours: Optional[int] = None
    start_date: Optional[datetime] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    
    @validator('hourly_rate')
    def validate_hourly_rate(cls, v):
        if v is None:
            return v
        if v < 0 or v > 10000:
            raise ValueError('Hourly rate must be between 0 and 10000')
        return v
    
    @validator('estimated_hours')
    def validate_estimated_hours(cls, v):
        if v is None:
            return v
        if v < 1 or v > 10000:
            raise ValueError('Estimated hours must be between 1 and 10000')
        return v
    
    @validator('contact_phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', v)
        # Check if it's a valid phone number (10-15 digits)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits')
        return v
    
    class Config:
        extra = "ignore"

class JobResponse(BaseModel):
    id: int
    business_owner_id: int
    title: str
    description: Optional[str] = None
    required_skills: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    hourly_rate: Optional[float] = None
    estimated_hours: Optional[int] = None
    start_date: Optional[datetime] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    posted_date: datetime
    status: str
    
    class Config:
        from_attributes = True

class JobUpdate(BaseModel):
    business_owner_id: Optional[int] = None
    title: Optional[str] = None
    description: Optional[str] = None
    required_skills: Optional[str] = None
    location: Optional[str] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    hourly_rate: Optional[float] = None
    estimated_hours: Optional[int] = None
    start_date: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    status: Optional[str] = None
    
    @validator('hourly_rate')
    def validate_hourly_rate(cls, v):
        if v is None:
            return v
        if v < 0 or v > 10000:
            raise ValueError('Hourly rate must be between 0 and 10000')
        return v
    
    @validator('estimated_hours')
    def validate_estimated_hours(cls, v):
        if v is None:
            return v
        if v < 1 or v > 10000:
            raise ValueError('Estimated hours must be between 1 and 10000')
        return v
    
    @validator('contact_phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', v)
        # Check if it's a valid phone number (10-15 digits)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits')
        return v
    
    class Config:
        extra = "ignore" 