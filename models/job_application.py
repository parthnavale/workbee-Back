from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.database import Base
from datetime import datetime

class JobApplication(Base):
    __tablename__ = "job_applications"
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=False)
    worker_id = Column(Integer, ForeignKey('workers.id'), nullable=False)
    status = Column(String(20), default="pending")
    applied_date = Column(DateTime, default=datetime.utcnow)
    responded_date = Column(DateTime)
    message = Column(String(500)) 