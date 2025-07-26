from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from core.database import Base
from datetime import datetime

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete="CASCADE"), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    status = Column(String(20), default="pending")
    applied_date = Column(DateTime, default=datetime.utcnow)
    responded_date = Column(DateTime)
    message = Column(String(500))
    
    # Add unique constraint to prevent duplicate applications
    __table_args__ = (
        UniqueConstraint('job_id', 'worker_id', name='unique_job_worker_application'),
    ) 