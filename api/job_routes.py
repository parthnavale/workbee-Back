from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.job_schemas import JobCreate, JobResponse, JobUpdate
from core.database import get_db
from models.job import Job
from models.business_owner import BusinessOwner
from models.job_application import JobApplication
from datetime import datetime
import h3
from sqlalchemy import and_
from models.worker import Worker
from models.notification import Notification
from schemas.notification_schemas import NotificationCreate

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    # Check if business owner exists
    business_owner = db.query(BusinessOwner).filter(BusinessOwner.id == job.business_owner_id).first()
    if not business_owner:
        raise HTTPException(status_code=400, detail=f"Business owner with id {job.business_owner_id} not found")
    
    try:
        db_job = Job(**job.dict())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)

        # --- H3 Geospatial Notification Logic ---
        if db_job.latitude is not None and db_job.longitude is not None:
            h3_resolution = 8  # Reasonable for city/neighborhood
            job_h3 = h3.latlng_to_cell(db_job.latitude, db_job.longitude, h3_resolution)
            workers = db.query(Worker).filter(and_(Worker.latitude != None, Worker.longitude != None)).all()
            neighbor_cells = set(h3.grid_disk(job_h3, 1))
            notify_worker_ids = []
            for worker in workers:
                worker_h3 = h3.latlng_to_cell(worker.latitude, worker.longitude, h3_resolution)
                if worker_h3 in neighbor_cells:
                    notify_worker_ids.append(worker.id)
                    # Create notification for this worker
                    notification = Notification(
                        worker_id=worker.id,
                        job_id=db_job.id,
                        message=f"New job nearby: {db_job.title}",
                        is_read=False
                    )
                    db.add(notification)
            db.commit()
            print(f"[H3] Notifying workers: {notify_worker_ids} for job {db_job.id}")
        # --- End H3 logic ---

        return db_job
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

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
def get_jobs_by_business_owner(business_owner_id: int, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.business_owner_id == business_owner_id).all()
    return jobs

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    try:
        for key, value in job_update.dict(exclude_unset=True).items():
            setattr(job, key, value)
        db.commit()
        db.refresh(job)
        return job
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Delete job and all associated applications"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get all applications for this job
    applications = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
    
    # Delete applications first (due to foreign key constraints)
    for application in applications:
        db.delete(application)
    
    # Delete job
    db.delete(job)
    db.commit()
    
    return {
        "success": True,
        "message": "Job and all associated applications deleted successfully",
        "deleted_job_id": job_id,
        "deleted_applications_count": len(applications),
        "deleted_at": datetime.utcnow().isoformat()
    } 