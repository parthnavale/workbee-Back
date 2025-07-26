from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base

class BusinessOwner(Base):
    __tablename__ = "business_owners"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    business_name = Column(String(100), nullable=False)
    contact_person = Column(String(100))
    contact_phone = Column(String(20))
    contact_email = Column(String(100))
    address = Column(String(200))
    website = Column(String(100))
    industry = Column(String(50))
    state = Column(String(50))
    city = Column(String(50))
    pincode = Column(String(20))
    year_established = Column(Integer) 