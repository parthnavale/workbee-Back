"""
Business Owner model module
Handles business owner specific data and relationships
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class BusinessOwner(Base):
    """
    Business Owner model for business-specific data
    Follows Single Responsibility Principle - only handles business owner data
    """
    __tablename__ = 'business_owners'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    company_name = Column(String(100), nullable=False)
    industry = Column(String(50), nullable=False)
    description = Column(Text)
    phone = Column(String(20))
    address = Column(String(200))
    website = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    user = relationship("User", back_populates="business_owner")
    jobs = relationship("Job", back_populates="business_owner", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="business_owner", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="business_owner", uselist=False)
    
    def __repr__(self):
        return f"<BusinessOwner(id={self.id}, company='{self.company_name}')>"
    
    @property
    def active_jobs_count(self) -> int:
        """Get count of active jobs"""
        return len([job for job in self.jobs if job.status.value == "active"])
    
    @property
    def total_jobs_count(self) -> int:
        """Get total count of jobs"""
        return len(self.jobs) 