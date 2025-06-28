"""
Worker model module
Handles worker specific data and relationships
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Worker(Base):
    """
    Worker model for worker-specific data
    Follows Single Responsibility Principle - only handles worker data
    """
    __tablename__ = 'workers'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    address = Column(String(200))
    skills = Column(JSON)  # Store as JSON array
    experience_years = Column(Integer, default=0)
    bio = Column(Text)
    hourly_rate = Column(Integer)  # Rate in cents
    availability = Column(JSON)  # Store availability schedule as JSON
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    user = relationship("User", back_populates="worker")
    applications = relationship("JobApplication", back_populates="worker", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Worker(id={self.id}, name='{self.first_name} {self.last_name}')>"
    
    @property
    def full_name(self) -> str:
        """Get full name of worker"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def hourly_rate_dollars(self) -> float:
        """Get hourly rate in dollars"""
        return self.hourly_rate / 100 if self.hourly_rate else 0.0
    
    @property
    def active_applications_count(self) -> int:
        """Get count of active applications"""
        return len([app for app in self.applications if app.status.value in ["pending", "accepted"]]) 