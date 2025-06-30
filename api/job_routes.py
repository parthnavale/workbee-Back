from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.job_schemas import JobCreate, JobResponse
from core.database import get_db
from models.job import Job

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/", response_model=list[JobResponse])
def get_all_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.get("/business/{business_owner_id}", response_model=list[JobResponse])
def get_jobs_by_business(business_owner_id: int, db: Session = Depends(get_db)):
    return db.query(Job).filter(Job.business_owner_id == business_owner_id).all()

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_update: JobCreate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(job, key, value)
    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    db.delete(job)
    db.commit()
    return {"detail": "Job deleted"} 