from sqlalchemy import Column, Integer, DateTime, ForeignKey
from database import Base

class Subscription(Base):
        __tablename__ = 'subscription'

        id = Column(Integer, primary_key= True, index=True)
        usinessRegistrationNumber = Column(Integer, ForeignKey("owner.id"), nullable=False)
        start = Column(DateTime(timezone=True))
        end = Column(DateTime(timezone=True))
        
