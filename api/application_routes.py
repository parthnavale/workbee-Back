from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.job_application_schemas import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate
from core.database import get_db
from models.job_application import JobApplication
from models.job import Job
from models.worker import Worker
from datetime import datetime

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=JobApplicationResponse)
def apply_for_job(application: JobApplicationCreate, db: Session = Depends(get_db)):
    # Check if job exists
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=400, detail=f"Job with id {application.job_id} not found")
    
    # Check if worker exists
    worker = db.query(Worker).filter(Worker.id == application.worker_id).first()
    if not worker:
        raise HTTPException(status_code=400, detail=f"Worker with id {application.worker_id} not found")
    
    # Check if application already exists
    existing_app = db.query(JobApplication).filter(
        JobApplication.job_id == application.job_id,
        JobApplication.worker_id == application.worker_id
    ).first()
    if existing_app:
        raise HTTPException(status_code=400, detail=f"Worker {application.worker_id} has already applied for job {application.job_id}")
    
    try:
        db_app = JobApplication(**application.dict())
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        return db_app
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    return app

@router.get("/", response_model=list[JobApplicationResponse])
def get_all_applications(db: Session = Depends(get_db)):
    return db.query(JobApplication).all()

@router.get("/job/{job_id}", response_model=list[JobApplicationResponse])
def get_applications_by_job(job_id: int, db: Session = Depends(get_db)):
    applications = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
    return applications

@router.get("/worker/{worker_id}", response_model=list[JobApplicationResponse])
def get_applications_by_worker(worker_id: int, db: Session = Depends(get_db)):
    applications = db.query(JobApplication).filter(JobApplication.worker_id == worker_id).all()
    return applications

@router.put("/{application_id}", response_model=JobApplicationResponse)
def update_application(application_id: int, application_update: JobApplicationUpdate, db: Session = Depends(get_db)):
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    try:
        for key, value in application_update.dict(exclude_unset=True).items():
            setattr(app, key, value)
        db.commit()
        db.refresh(app)
        return app
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete a job application"""
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Store application details before deletion for response
    job_id = app.job_id
    worker_id = app.worker_id
    
    # Delete application
    db.delete(app)
    db.commit()
    
    return {
        "success": True,
        "message": "Job application deleted successfully",
        "deleted_application_id": application_id,
        "job_id": job_id,
        "worker_id": worker_id,
        "deleted_at": datetime.utcnow().isoformat()
    } 