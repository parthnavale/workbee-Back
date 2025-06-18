from sqlalchemy import Column, Integer, String, Enum
from database import Base
import enum


#add enums
class SkillEnum(str, enum.Enum):
    PLUMBING = "Construction Worker"
    ELECTRICAL = "Warehouse Assistant"
    PAINTING = "PAINTING"

class Worker(Base):
        __tablename__ = 'worker'

        #id proof
        id = Column(Integer, primary_key= True, index=True)
        description = Column(String(500), nullable=False)
        name = Column(String(100),nullable=False)
        state = Column(String(100), nullable=False)
        city = Column(String(100), nullable=False)

        # enum handled in main.py
        skills = Column(String(100), nullable=False)