from pydantic import BaseModel
from typing import Optional

class BusinessOwnerCreate(BaseModel):
    user_id: int
    business_name: str
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    year_established: Optional[int] = None
    class Config:
        extra = "ignore"

class BusinessOwnerResponse(BusinessOwnerCreate):
    id: int
    class Config:
        from_attributes = True 