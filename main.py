from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from enum import Enum
from typing import Annotated, List
import models
import Job
import BusinessOwner
import subscription
import Worker
from database import engine, Sessionlocal
from sqlalchemy.orm import Session

app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind = engine)
Job.Base.metadata.create_all(bind = engine)
BusinessOwner.Base.metadata.create_all(bind = engine)
subscription.Base.metadata.create_all(bind = engine)
Worker.Base.metadata.create_all(bind = engine)



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

def get_db():
    db = Sessionlocal()
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
async def read_job(db: db_dependency):
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
async def delete_post(user_Id: int, db: db_dependency):
    db_user = db.query(models.User).filter(models.User.id == user_Id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail='User was not found')
    db.delete(db_user)
    db.commit()

