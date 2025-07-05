from pydantic import BaseModel, validator
from typing import Optional
import re

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
    
    @validator('contact_phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', v)
        # Check if it's a valid phone number (10 digits for India, 10-15 for international)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits (10 digits for India)')
        # For Indian numbers, ensure they start with 6, 7, 8, or 9
        if len(digits_only) == 10:
            if not digits_only.startswith(('6', '7', '8', '9')):
                raise ValueError('Indian phone numbers must start with 6, 7, 8, or 9')
        return v
    
    @validator('year_established')
    def validate_year(cls, v):
        if v is None:
            return v
        if v < 1800 or v > 2100:
            raise ValueError('Year must be between 1800 and 2100')
        return v
    
    class Config:
        extra = "ignore"

class BusinessOwnerUpdate(BaseModel):
    business_name: Optional[str] = None
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
    
    @validator('contact_phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', v)
        # Check if it's a valid phone number (10 digits for India, 10-15 for international)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits (10 digits for India)')
        # For Indian numbers, ensure they start with 6, 7, 8, or 9
        if len(digits_only) == 10:
            if not digits_only.startswith(('6', '7', '8', '9')):
                raise ValueError('Indian phone numbers must start with 6, 7, 8, or 9')
        return v
    
    @validator('year_established')
    def validate_year(cls, v):
        if v is None:
            return v
        if v < 1800 or v > 2100:
            raise ValueError('Year must be between 1800 and 2100')
        return v
    
    class Config:
        extra = "ignore"

class BusinessOwnerResponse(BaseModel):
    id: int
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
        from_attributes = True 