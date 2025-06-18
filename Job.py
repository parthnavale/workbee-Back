from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

#Add enum for the typeof business , city and state in front end

class Job(Base):
        __tablename__ = 'job'

        #manually create it 
        id = Column(Integer, primary_key= True, index=True)
        description = Column(String(400),nullable=False)
        #businessRegistrationNumber = Column(Integer)
        businessRegistrationNumber = Column(Integer, ForeignKey("owner.id"), nullable=False)
        #add enum in frontend
        role = Column(String(100),nullable=False)
        # add enumber for the below in flutter front end 
        typeOfBusiness = Column(String(100),nullable=False)
        state =  Column(String(100), nullable=False)
        city =  Column(String(100), nullable=False)
        pincode = Column(Integer, nullable=False)
