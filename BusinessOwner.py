from sqlalchemy import Column, Integer, String
from database import Base

#Add enum for the typeof business , city and state in front end

class BusinessOwner(Base):
        __tablename__ = 'owner'

        #registration number
        id = Column(Integer, primary_key= True, index=True)
        role = Column(String(100),nullable=False)
        name = Column(String(100),nullable=False)
        phoneNumber = Column(String(100),nullable=False)
        #year of establishment
        year = Column(Integer, nullable=False)
        typeOfBusiness = Column(String(100),nullable=False)
        state =  Column(String(100), nullable=False)
        city =  Column(String(100), nullable=False)
        pincode = Column(Integer, nullable=False)
