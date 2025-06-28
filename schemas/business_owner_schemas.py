"""
Business Owner schemas module
Handles Pydantic schemas for business owner data validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BusinessOwnerBase(BaseModel):
    """Base business owner schema with common fields"""
    company_name: str
    industry: str
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None

class BusinessOwnerCreate(BusinessOwnerBase):
    """Schema for creating a new business owner"""
    user_id: int

class BusinessOwnerUpdate(BaseModel):
    """Schema for updating business owner data"""
    company_name: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    website: Optional[str] = None

class BusinessOwnerResponse(BusinessOwnerBase):
    """Schema for business owner response data"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 