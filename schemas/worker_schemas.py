from pydantic import BaseModel, validator
from typing import Optional
import re

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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fcm_token: Optional[str] = None

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', v)
        # Check if it's a valid phone number (10-15 digits)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits')
        return v

    @validator('years_of_experience')
    def validate_experience(cls, v):
        if v is None:
            return v
        if v < 0 or v > 100:
            raise ValueError('Years of experience must be between 0 and 100')
        return v

    @validator('latitude')
    def validate_latitude(cls, v):
        if v is None:
            return v
        if v < -90 or v > 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if v is None:
            return v
        if v < -180 or v > 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

    class Config:
        extra = "ignore"

class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    skills: Optional[str] = None
    years_of_experience: Optional[int] = None
    address: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    pincode: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fcm_token: Optional[str] = None

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        # Remove all non-digit characters
        digits_only = re.sub(r'\D', '', v)
        # Check if it's a valid phone number (10-15 digits)
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('Phone number must be 10-15 digits')
        return v

    @validator('years_of_experience')
    def validate_experience(cls, v):
        if v is None:
            return v
        if v < 0 or v > 100:
            raise ValueError('Years of experience must be between 0 and 100')
        return v

    @validator('latitude')
    def validate_latitude(cls, v):
        if v is None:
            return v
        if v < -90 or v > 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        if v is None:
            return v
        if v < -180 or v > 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v

    class Config:
        extra = "ignore"

class WorkerResponse(BaseModel):
    id: int
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
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    fcm_token: Optional[str] = None

    class Config:
        from_attributes = True 