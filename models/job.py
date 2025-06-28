"""
Job model module
Handles job data and status management
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Numeric, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base

class JobStatus(str, enum.Enum):
    """Job status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Job(Base):
    """
    Job model for job posting and management
    Follows Single Responsibility Principle - only handles job data
    """
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    business_owner_id = Column(Integer, ForeignKey('business_owners.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(Text)
    location = Column(String(100))
    job_type = Column(String(50))  # full-time, part-time, contract, etc.
    salary_min = Column(Integer)  # Salary in cents
    salary_max = Column(Integer)  # Salary in cents
    hourly_rate = Column(Integer)  # Hourly rate in cents
    duration = Column(String(50))  # Duration of the job
    skills_required = Column(JSON)  # Store as JSON array
    status = Column(Enum(JobStatus), default=JobStatus.ACTIVE)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    business_owner = relationship("BusinessOwner", back_populates="jobs")
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', status='{self.status}')>"
    
    @property
    def salary_range_dollars(self) -> tuple:
        """Get salary range in dollars"""
        min_salary = self.salary_min / 100 if self.salary_min else 0.0
        max_salary = self.salary_max / 100 if self.salary_max else 0.0
        return (min_salary, max_salary)
    
    @property
    def hourly_rate_dollars(self) -> float:
        """Get hourly rate in dollars"""
        return self.hourly_rate / 100 if self.hourly_rate else 0.0
    
    @property
    def applications_count(self) -> int:
        """Get count of applications"""
        return len(self.applications)
    
    @property
    def is_active(self) -> bool:
        """Check if job is active"""
        return self.status == JobStatus.ACTIVE 