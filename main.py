from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated, List, Optional
from datetime import datetime
import json
from sqlalchemy.orm import Session
from core.database import engine, SessionLocal, Base
import models
import Job
import BusinessOwner
import Subscription
import Worker

app = FastAPI(title="WorkShift API", version="2.0.0")
# models.Base.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)
Job.Base.metadata.create_all(bind = engine)
BusinessOwner.Base.metadata.create_all(bind = engine)
Subscription.Base.metadata.create_all(bind = engine)
Worker.Base.metadata.create_all(bind = engine)

# Add CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobBase(BaseModel):
    id: int
    description: str 
    businessRegistrationNumber: int
    role: str  # Should match Flutter enum
    typeOfBusiness: str  # Should match Flutter enum
    state: str
    city: str
    pincode: int

class PostBase(BaseModel):
    title: str
    content: str
    user_Id: int

class UserBase(BaseModel):
    #id: int
    username: str

class BusinessOwnerBase(BaseModel):
    id: int
    role : str
    name : str
    phoneNumber : str
    year: int
    typeOfBusiness: str
    state: str
    city: str
    pincode: int

class WorkerBase(BaseModel):
    id: int
    description: str
    name: str
    state: str
    city: str
    skills: str

class SubscriptionBase(BaseModel):
    id: int
    clientId: int
    start: datetime
    end: datetime

def get_db():
    db = SessionLocal()
    try: 
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/job/{job_id}", status_code=status.HTTP_200_OK)
async def read_job(job_id: int, db: db_dependency):
    job = db.query(Job.Job).filter(Job.Job.id == job_id).first()
    if job is None:
        HTTPException(status_code=404, detail='Job was not found')
    return job

@app.get("/job", status_code=status.HTTP_200_OK)
async def read_joball(db: db_dependency):
    job = db.query(Job.Job)
    if job is None:
        HTTPException(status_code=404, detail='Job was not found')
    return job


@app.post("/job/", status_code=status.HTTP_201_CREATED)
async def create_job(job: JobBase, db: db_dependency):
    db_job = Job.Job(**job.dict())
    db.add(db_job)
    db.commit()

@app.get("/owner/{owner_id}", status_code=status.HTTP_200_OK)
async def read_owner(owner_id: int, db:db_dependency):
    owner = db.query(BusinessOwner.BusinessOwner).filter(BusinessOwner.BusinessOwner.id == owner_id).first()
    if owner is None:
        HTTPException(status_code=404, detail='Owner was not found')
    return owner

@app.post("/subscription/", status_code=status.HTTP_201_CREATED)
async def create_subscription(subscription: SubscriptionBase, db: db_dependency):
    db_subscritption = Subscription.Subscription(**subscription.dict())
    db.add(db_subscritption)
    db.commit()

@app.get("/subscription/{subscription_id}", status_code=status.HTTP_200_OK)
async def read_subscription(subscription_id: int, db:db_dependency):
    subscription = db.query(Subscription.Subscription).filter(Subscription.Subscription.id == subscription_id).first()
    if subscription is None:
        HTTPException(status_code=404, detail='Subscription was not found')
    return subscription

@app.post("/owner/", status_code=status.HTTP_201_CREATED)
async def create_owner(owner: BusinessOwnerBase , db: db_dependency):
    db_owner = BusinessOwner.BusinessOwner(**owner.dict())
    db.add(db_owner)
    db.commit()

@app.get("/worker/{worker_id}", status_code=status.HTTP_200_OK)
async def read_worker(worker_id: int, db:db_dependency):
    worker = db.query(Worker.Worker).filter(Worker.Worker.id == worker_id).first()
    if worker is None:
        HTTPException(status_code=404, detail='Job was not found')
    return worker

@app.post("/worker/", status_code=status.HTTP_201_CREATED)
async def create_worker(worker: WorkerBase , db: db_dependency):
    db_worker = Worker.Worker(**worker.dict())
    db.add(db_worker)
    db.commit()


@app.get("/posts/{post_Id}", status_code= status.HTTP_200_OK)
async def read_post(post_Id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_Id).first()
    if post is None:
        HTTPException(status_code=404, detail='Post was not found')
    return post


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostBase, db: db_dependency):
    db_post = models.Post(**post.dict())
    db.add(db_post)
    db.commit()

@app.delete("/posts/{post_Id}", status_code= status.HTTP_200_OK)
async def delete_post(post_Id: int, db: db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_Id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail='Post was not found')
    db.delete(db_post)
    db.commit()



@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()


@app.get("/users/{user_Id}", status_code= status.HTTP_201_CREATED)
async def read_user(user_Id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_Id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

@app.delete("/users/{user_Id}", status_code= status.HTTP_200_OK)
async def delete_user(user_Id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_Id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.delete(db_user)
    db.commit()

# Pydantic models for request/response
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class BusinessOwnerCreate(BaseModel):
    user_id: int
    business_name: str
    business_registration_number: str
    contact_person: str
    contact_phone: str
    contact_email: str
    type_of_business: str
    year_established: int
    state: str
    city: str
    pincode: str
    address: str

class BusinessOwnerResponse(BaseModel):
    id: int
    business_name: str
    business_registration_number: str
    contact_person: str
    contact_phone: str
    contact_email: str
    type_of_business: str
    year_established: int
    state: str
    city: str
    pincode: str
    address: str
    created_at: datetime

    class Config:
        from_attributes = True

class WorkerCreate(BaseModel):
    user_id: int
    name: str
    phone: str
    email: str
    skills: List[str]
    years_of_experience: int = 0
    previous_work_experience: Optional[str] = None
    state: str
    city: str
    pincode: str
    address: str

class WorkerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    skills: List[str]
    years_of_experience: int
    previous_work_experience: Optional[str]
    state: str
    city: str
    pincode: str
    address: str
    is_available: bool
    created_at: datetime

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    business_owner_id: int
    title: str
    description: str
    required_skills: List[str]
    location: str
    address: str
    state: str
    city: str
    pincode: str
    hourly_rate: float
    estimated_hours: int
    start_date: Optional[datetime] = None
    contact_person: str
    contact_phone: str
    contact_email: str

class JobResponse(BaseModel):
    id: int
    business_owner_id: int
    business_name: str
    title: str
    description: str
    required_skills: List[str]
    location: str
    address: str
    state: str
    city: str
    pincode: str
    hourly_rate: float
    estimated_hours: int
    posted_date: datetime
    start_date: Optional[datetime]
    status: str
    contact_person: str
    contact_phone: str
    contact_email: str
    created_at: datetime

    class Config:
        from_attributes = True

class JobApplicationCreate(BaseModel):
    job_id: int
    worker_id: int
    message: Optional[str] = None

class JobApplicationResponse(BaseModel):
    id: int
    job_id: int
    worker_id: int
    worker_name: str
    worker_email: str
    worker_phone: str
    worker_skills: List[str]
    years_of_experience: int
    previous_work_experience: Optional[str]
    status: str
    applied_date: datetime
    responded_date: Optional[datetime]
    message: Optional[str]

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    job_id: int
    application_id: int
    status: str
    message: Optional[str] = None

# Helper functions
def skills_to_json(skills: List[str]) -> str:
    return json.dumps(skills)

def json_to_skills(skills_json: str) -> List[str]:
    try:
        return json.loads(skills_json)
    except:
        return []

# User endpoints
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email,
        password_hash=user.password,  # In production, hash the password
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Business Owner endpoints
@app.post("/business-owners/", response_model=BusinessOwnerResponse, status_code=status.HTTP_201_CREATED)
async def create_business_owner(owner: BusinessOwnerCreate, db: Session = Depends(get_db)):
    db_owner = models.BusinessOwner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

@app.get("/business-owners/{owner_id}", response_model=BusinessOwnerResponse)
async def get_business_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(models.BusinessOwner).filter(models.BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    return owner

# Worker endpoints
@app.post("/workers/", response_model=WorkerResponse, status_code=status.HTTP_201_CREATED)
async def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    worker_data = worker.dict()
    worker_data['skills'] = skills_to_json(worker_data['skills'])
    db_worker = models.Worker(**worker_data)
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    
    # Convert back for response
    response_data = worker.dict()
    response_data['id'] = db_worker.id
    response_data['is_available'] = db_worker.is_available
    response_data['created_at'] = db_worker.created_at
    return response_data

@app.get("/workers/{worker_id}", response_model=WorkerResponse)
async def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(models.Worker).filter(models.Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Convert skills back to list
    response_data = {
        'id': worker.id,
        'name': worker.name,
        'phone': worker.phone,
        'email': worker.email,
        'skills': json_to_skills(worker.skills),
        'years_of_experience': worker.years_of_experience,
        'previous_work_experience': worker.previous_work_experience,
        'state': worker.state,
        'city': worker.city,
        'pincode': worker.pincode,
        'address': worker.address,
        'is_available': worker.is_available,
        'created_at': worker.created_at
    }
    return response_data

# Job endpoints
@app.post("/jobs/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(job: JobCreate, db: Session = Depends(get_db)):
    job_data = job.dict()
    job_data['required_skills'] = skills_to_json(job_data['required_skills'])
    db_job = models.Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    # Get business owner name
    business_owner = db.query(models.BusinessOwner).filter(
        models.BusinessOwner.id == db_job.business_owner_id
    ).first()
    
    # Convert back for response
    response_data = job.dict()
    response_data['id'] = db_job.id
    response_data['business_name'] = business_owner.business_name if business_owner else "Unknown"
    response_data['posted_date'] = db_job.posted_date
    response_data['status'] = db_job.status.value
    response_data['created_at'] = db_job.created_at
    return response_data

@app.get("/jobs/", response_model=List[JobResponse])
async def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    response_jobs = []
    
    for job in jobs:
        business_owner = db.query(models.BusinessOwner).filter(
            models.BusinessOwner.id == job.business_owner_id
        ).first()
        
        response_data = {
            'id': job.id,
            'business_owner_id': job.business_owner_id,
            'business_name': business_owner.business_name if business_owner else "Unknown",
            'title': job.title,
            'description': job.description,
            'required_skills': json_to_skills(job.required_skills),
            'location': job.location,
            'address': job.address,
            'state': job.state,
            'city': job.city,
            'pincode': job.pincode,
            'hourly_rate': job.hourly_rate,
            'estimated_hours': job.estimated_hours,
            'posted_date': job.posted_date,
            'start_date': job.start_date,
            'status': job.status.value,
            'contact_person': job.contact_person,
            'contact_phone': job.contact_phone,
            'contact_email': job.contact_email,
            'created_at': job.created_at
        }
        response_jobs.append(response_data)
    
    return response_jobs

@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    business_owner = db.query(models.BusinessOwner).filter(
        models.BusinessOwner.id == job.business_owner_id
    ).first()
    
    response_data = {
        'id': job.id,
        'business_owner_id': job.business_owner_id,
        'business_name': business_owner.business_name if business_owner else "Unknown",
        'title': job.title,
        'description': job.description,
        'required_skills': json_to_skills(job.required_skills),
        'location': job.location,
        'address': job.address,
        'state': job.state,
        'city': job.city,
        'pincode': job.pincode,
        'hourly_rate': job.hourly_rate,
        'estimated_hours': job.estimated_hours,
        'posted_date': job.posted_date,
        'start_date': job.start_date,
        'status': job.status.value,
        'contact_person': job.contact_person,
        'contact_phone': job.contact_phone,
        'contact_email': job.contact_email,
        'created_at': job.created_at
    }
    return response_data

@app.get("/jobs/business/{business_owner_id}", response_model=List[JobResponse])
async def get_jobs_by_business(business_owner_id: int, db: Session = Depends(get_db)):
    jobs = db.query(models.Job).filter(models.Job.business_owner_id == business_owner_id).all()
    response_jobs = []
    
    for job in jobs:
        business_owner = db.query(models.BusinessOwner).filter(
            models.BusinessOwner.id == job.business_owner_id
        ).first()
        
        response_data = {
            'id': job.id,
            'business_owner_id': job.business_owner_id,
            'business_name': business_owner.business_name if business_owner else "Unknown",
            'title': job.title,
            'description': job.description,
            'required_skills': json_to_skills(job.required_skills),
            'location': job.location,
            'address': job.address,
            'state': job.state,
            'city': job.city,
            'pincode': job.pincode,
            'hourly_rate': job.hourly_rate,
            'estimated_hours': job.estimated_hours,
            'posted_date': job.posted_date,
            'start_date': job.start_date,
            'status': job.status.value,
            'contact_person': job.contact_person,
            'contact_phone': job.contact_phone,
            'contact_email': job.contact_email,
            'created_at': job.created_at
        }
        response_jobs.append(response_data)
    
    return response_jobs

# Job Application endpoints
@app.post("/job-applications/", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_job_application(application: JobApplicationCreate, db: Session = Depends(get_db)):
    db_application = models.JobApplication(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    
    # Get worker details
    worker = db.query(models.Worker).filter(models.Worker.id == db_application.worker_id).first()
    
    response_data = {
        'id': db_application.id,
        'job_id': db_application.job_id,
        'worker_id': db_application.worker_id,
        'worker_name': worker.name if worker else "Unknown",
        'worker_email': worker.email if worker else "",
        'worker_phone': worker.phone if worker else "",
        'worker_skills': json_to_skills(worker.skills) if worker else [],
        'years_of_experience': worker.years_of_experience if worker else 0,
        'previous_work_experience': worker.previous_work_experience if worker else None,
        'status': db_application.status.value,
        'applied_date': db_application.applied_date,
        'responded_date': db_application.responded_date,
        'message': db_application.message
    }
    return response_data

@app.get("/job-applications/job/{job_id}", response_model=List[JobApplicationResponse])
async def get_applications_for_job(job_id: int, db: Session = Depends(get_db)):
    applications = db.query(models.JobApplication).filter(
        models.JobApplication.job_id == job_id
    ).all()
    
    response_applications = []
    for application in applications:
        worker = db.query(models.Worker).filter(models.Worker.id == application.worker_id).first()
        
        response_data = {
            'id': application.id,
            'job_id': application.job_id,
            'worker_id': application.worker_id,
            'worker_name': worker.name if worker else "Unknown",
            'worker_email': worker.email if worker else "",
            'worker_phone': worker.phone if worker else "",
            'worker_skills': json_to_skills(worker.skills) if worker else [],
            'years_of_experience': worker.years_of_experience if worker else 0,
            'previous_work_experience': worker.previous_work_experience if worker else None,
            'status': application.status.value,
            'applied_date': application.applied_date,
            'responded_date': application.responded_date,
            'message': application.message
        }
        response_applications.append(response_data)
    
    return response_applications

@app.put("/job-applications/{application_id}/respond", response_model=JobApplicationResponse)
async def respond_to_application(
    application_id: int, 
    response: ApplicationResponse, 
    db: Session = Depends(get_db)
):
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id
    ).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
    application.status = response.status
    application.responded_date = datetime.utcnow()
    application.message = response.message
    
    db.commit()
    db.refresh(application)
    
    # Get worker details
    worker = db.query(models.Worker).filter(models.Worker.id == application.worker_id).first()
    
    response_data = {
        'id': application.id,
        'job_id': application.job_id,
        'worker_id': application.worker_id,
        'worker_name': worker.name if worker else "Unknown",
        'worker_email': worker.email if worker else "",
        'worker_phone': worker.phone if worker else "",
        'worker_skills': json_to_skills(worker.skills) if worker else [],
        'years_of_experience': worker.years_of_experience if worker else 0,
        'previous_work_experience': worker.previous_work_experience if worker else None,
        'status': application.status.value,
        'applied_date': application.applied_date,
        'responded_date': application.responded_date,
        'message': application.message
    }
    return response_data

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

