"""
User model module
Handles user authentication and role management
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base

class UserRole(str, enum.Enum):
    """User role enumeration"""
    BUSINESS_OWNER = "business_owner"
    WORKER = "worker"
    ADMIN = "admin"

class User(Base):
    """
    User model for authentication and role management
    Follows Single Responsibility Principle - only handles user data
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    business_owner = relationship("BusinessOwner", back_populates="user", uselist=False)
    worker = relationship("Worker", back_populates="user", uselist=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    @property
    def is_business_owner(self) -> bool:
        """Check if user is a business owner"""
        return self.role == UserRole.BUSINESS_OWNER
    
    @property
    def is_worker(self) -> bool:
        """Check if user is a worker"""
        return self.role == UserRole.WORKER
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.role == UserRole.ADMIN 