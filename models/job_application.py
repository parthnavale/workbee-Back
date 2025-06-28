"""
Job Application model module
Handles job application data and status management
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base

class ApplicationStatus(str, enum.Enum):
    """Application status enumeration"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class JobApplication(Base):
    """
    Job Application model for managing job applications
    Follows Single Responsibility Principle - only handles application data
    """
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    cover_letter = Column(Text)
    resume_url = Column(String(255))
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING)
    applied_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    job = relationship("Job", back_populates="applications")
    worker = relationship("Worker", back_populates="applications")
    
    def __repr__(self):
        return f"<JobApplication(id={self.id}, job_id={self.job_id}, worker_id={self.worker_id}, status='{self.status}')>"
    
    @property
    def is_pending(self) -> bool:
        """Check if application is pending"""
        return self.status == ApplicationStatus.PENDING
    
    @property
    def is_accepted(self) -> bool:
        """Check if application is accepted"""
        return self.status == ApplicationStatus.ACCEPTED
    
    @property
    def is_rejected(self) -> bool:
        """Check if application is rejected"""
        return self.status == ApplicationStatus.REJECTED
    
    @property
    def is_withdrawn(self) -> bool:
        """Check if application is withdrawn"""
        return self.status == ApplicationStatus.WITHDRAWN 