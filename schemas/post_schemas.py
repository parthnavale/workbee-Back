"""
Post schemas module
Handles Pydantic schemas for post data validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class PostBase(BaseModel):
    """Base post schema with common fields"""
    title: str
    content: str
    media_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class PostCreate(PostBase):
    """Schema for creating a new post"""
    business_owner_id: int

class PostUpdate(BaseModel):
    """Schema for updating post data"""
    title: Optional[str] = None
    content: Optional[str] = None
    media_urls: Optional[List[str]] = None
    tags: Optional[List[str]] = None

class PostResponse(PostBase):
    """Schema for post response data"""
    id: int
    business_owner_id: int
    likes_count: int
    shares_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True 