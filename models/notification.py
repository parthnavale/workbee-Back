from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, index=True)
    worker_id = Column(Integer, ForeignKey('workers.id', ondelete="CASCADE"), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id', ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    worker = relationship('Worker')
    job = relationship('Job') 