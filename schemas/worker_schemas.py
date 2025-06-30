from pydantic import BaseModel
from typing import Optional

class WorkerCreate(BaseModel):
    user_id: int
    name: str
    phone: Optional[str] = None
    email: Optional[str] = None
    skills: Optional[str] = None
    years_of_experience: Optional[int] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None

class WorkerResponse(WorkerCreate):
    id: int
    class Config:
        from_attributes = True 