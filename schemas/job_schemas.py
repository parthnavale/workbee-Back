from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    class Config:
        extra = "ignore"

class JobResponse(JobCreate):
    id: int
    posted_date: datetime
    status: str
    class Config:
        from_attributes = True 