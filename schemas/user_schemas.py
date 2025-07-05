from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    
    @validator('username')
    def validate_username(cls, v):
        if not v:
            raise ValueError('Username cannot be empty')
        if len(v) > 50:
            raise ValueError('Username must be 50 characters or less')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        # Allow alphanumeric, underscore, hyphen, and some special characters
        if not re.match(r'^[a-zA-Z0-9_\-\.!@#$%^&*()+=]+$', v):
            raise ValueError('Username contains invalid characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        if len(v) > 1000:  # Reasonable limit for password length
            raise ValueError('Password is too long')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        valid_roles = ['poster', 'seeker']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v
    
    class Config:
        extra = "ignore"

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if v is None:
            return v
        if len(v) > 50:
            raise ValueError('Username must be 50 characters or less')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters')
        # Allow alphanumeric, underscore, hyphen, and some special characters
        if not re.match(r'^[a-zA-Z0-9_\-\.!@#$%^&*()+=]+$', v):
            raise ValueError('Username contains invalid characters')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v) > 1000:  # Reasonable limit for password length
            raise ValueError('Password is too long')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        if v is None:
            return v
        valid_roles = ['poster', 'seeker']
        if v not in valid_roles:
            raise ValueError(f'Role must be one of: {", ".join(valid_roles)}')
        return v
    
    class Config:
        extra = "ignore"

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if not v:
            raise ValueError('Password cannot be empty')
        if len(v) > 1000:
            raise ValueError('Password is too long')
        return v
    
    class Config:
        extra = "ignore"

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    
    class Config:
        from_attributes = True 