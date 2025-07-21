from sqlalchemy import Column, Integer, String, ForeignKey, Float
from core.database import Base

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    skills = Column(String(200))  # Comma-separated
    years_of_experience = Column(Integer)
    address = Column(String(200))
    state = Column(String(50))
    city = Column(String(50))
    pincode = Column(String(20))
    latitude = Column(Float)
    longitude = Column(Float)
    fcm_token = Column(String(256), nullable=True) 