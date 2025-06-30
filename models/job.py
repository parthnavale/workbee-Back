from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from core.database import Base
from datetime import datetime

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    business_owner_id = Column(Integer, ForeignKey('business_owners.id'), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    required_skills = Column(String(200))  # Comma-separated
    location = Column(String(100))
    address = Column(String(200))
    state = Column(String(50))
    city = Column(String(50))
    pincode = Column(String(20))
    hourly_rate = Column(Float)
    estimated_hours = Column(Integer)
    posted_date = Column(DateTime, default=datetime.utcnow)
    start_date = Column(DateTime)
    status = Column(String(20), default="open")
    contact_person = Column(String(100))
    contact_phone = Column(String(20))
    contact_email = Column(String(100)) 