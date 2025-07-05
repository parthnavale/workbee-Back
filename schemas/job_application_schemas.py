from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobApplicationCreate(BaseModel):
    job_id: int
    worker_id: int
    message: Optional[str] = None
    class Config:
        extra = "ignore"

class JobApplicationResponse(JobApplicationCreate):
    id: int
    status: str
    applied_date: datetime
    responded_date: Optional[datetime] = None
    class Config:
        from_attributes = True

class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None 