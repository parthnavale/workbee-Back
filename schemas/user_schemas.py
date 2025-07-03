from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    class Config:
        extra = "ignore"

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        extra = "ignore"

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    class Config:
        from_attributes = True 