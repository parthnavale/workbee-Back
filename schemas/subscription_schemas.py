"""
Subscription schemas module
Handles Pydantic schemas for subscription data validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.subscription import SubscriptionType, SubscriptionStatus

class SubscriptionBase(BaseModel):
    """Base subscription schema with common fields"""
    subscription_type: SubscriptionType
    status: Optional[SubscriptionStatus] = SubscriptionStatus.ACTIVE
    start_date: datetime
    end_date: datetime
    auto_renew: Optional[bool] = True

class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a new subscription"""
    business_owner_id: int

class SubscriptionUpdate(BaseModel):
    """Schema for updating subscription data"""
    subscription_type: Optional[SubscriptionType] = None
    status: Optional[SubscriptionStatus] = None
    end_date: Optional[datetime] = None
    auto_renew: Optional[bool] = None

class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription response data"""
    id: int
    business_owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 