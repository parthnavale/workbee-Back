from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.job_application_schemas import JobApplicationCreate, JobApplicationResponse, JobApplicationUpdate
from core.database import get_db
from models.job_application import JobApplication
from models.job import Job
from models.worker import Worker
from datetime import datetime
from models.business_owner import BusinessOwner
from core.fcm import send_fcm_notification
from api.auth import require_worker, require_business_owner, get_current_user
from models.user import User

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=JobApplicationResponse)
def apply_for_job(
    application: JobApplicationCreate, 
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    # Check if job exists
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise HTTPException(status_code=400, detail=f"Job with id {application.job_id} not found")
    
    # Check if worker exists and belongs to current user
    worker = db.query(Worker).filter(
        Worker.id == application.worker_id,
        Worker.user_id == current_user.id
    ).first()
    if not worker:
        raise HTTPException(status_code=403, detail="You can only apply for jobs using your own worker profile")
    
    # Check if application already exists
    existing_app = db.query(JobApplication).filter(
        JobApplication.job_id == application.job_id,
        JobApplication.worker_id == application.worker_id
    ).first()
    if existing_app:
        raise HTTPException(status_code=400, detail=f"You have already applied for this job")
    
    try:
        db_app = JobApplication(**application.dict())
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        # Send FCM notification to business owner if they have an FCM token
        owner = db.query(BusinessOwner).filter(BusinessOwner.id == job.business_owner_id).first()
        if owner and owner.fcm_token:
            title = f"New Application for {job.title}"
            body = f"{worker.name or 'A worker'} has applied for your job: {job.title}."
            data = {
                "job_id": str(job.id),
                "application_id": str(db_app.id),
                "worker_id": str(worker.id)
            }
            send_fcm_notification(owner.fcm_token, title, body, data)
        return db_app
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.get("/my-applications", response_model=list[JobApplicationResponse])
def get_my_applications(
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    """Get current user's applications (workers only)"""
    # Get worker profile
    worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker profile not found")
    
    # Get applications for this worker
    applications = db.query(JobApplication).filter(JobApplication.worker_id == worker.id).all()
    return applications

@router.get("/job/{job_id}", response_model=list[JobApplicationResponse])
def get_applications_by_job(
    job_id: int,
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    """Get applications for a specific job (only if you own the job)"""
    # Check if job exists and belongs to current user
    job = db.query(Job).join(BusinessOwner).filter(
        Job.id == job_id,
        BusinessOwner.user_id == current_user.id
    ).first()
    if not job:
        raise HTTPException(status_code=403, detail="You can only view applications for your own jobs")
    
    applications = db.query(JobApplication).filter(JobApplication.job_id == job_id).all()
    return applications

@router.get("/worker/{worker_id}", response_model=list[JobApplicationResponse])
def get_applications_by_worker(
    worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get applications by worker ID (only if you own the worker profile or are admin)"""
    # Check if worker belongs to current user or user is admin
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    if worker.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    applications = db.query(JobApplication).filter(JobApplication.worker_id == worker_id).all()
    return applications

@router.get("/{application_id}", response_model=JobApplicationResponse)
def get_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get application by ID (only if you own it or are admin)"""
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if current user owns this application or is admin
    worker = db.query(Worker).filter(Worker.id == app.worker_id).first()
    if worker and worker.user_id == current_user.id:
        return app  # Worker can view their own application
    
    # Check if current user owns the job
    job = db.query(Job).join(BusinessOwner).filter(
        Job.id == app.job_id,
        BusinessOwner.user_id == current_user.id
    ).first()
    if job:
        return app  # Business owner can view applications for their jobs
    
    # Admin can view all applications
    if current_user.role == "admin":
        return app
    
    raise HTTPException(status_code=403, detail="Access denied")

@router.put("/{application_id}", response_model=JobApplicationResponse)
def update_application(
    application_id: int, 
    application_update: JobApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update application (only if you own the job or are admin)"""
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if current user owns the job
    job = db.query(Job).join(BusinessOwner).filter(
        Job.id == app.job_id,
        BusinessOwner.user_id == current_user.id
    ).first()
    if not job and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can only update applications for your own jobs")
    
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
def delete_application(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a job application (only if you own it or are admin)"""
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    # Check if current user owns this application
    worker = db.query(Worker).filter(Worker.id == app.worker_id).first()
    if worker and worker.user_id == current_user.id:
        # Worker can delete their own application
        db.delete(app)
        db.commit()
        return {
            "success": True,
            "message": "Application deleted successfully",
            "deleted_application_id": application_id,
            "deleted_at": datetime.utcnow().isoformat()
        }
    
    # Check if current user owns the job
    job = db.query(Job).join(BusinessOwner).filter(
        Job.id == app.job_id,
        BusinessOwner.user_id == current_user.id
    ).first()
    if job:
        # Business owner can delete applications for their jobs
        db.delete(app)
        db.commit()
        return {
            "success": True,
            "message": "Application deleted successfully",
            "deleted_application_id": application_id,
            "deleted_at": datetime.utcnow().isoformat()
        }
    
    # Admin can delete any application
    if current_user.role == "admin":
        db.delete(app)
        db.commit()
        return {
            "success": True,
            "message": "Application deleted successfully",
            "deleted_application_id": application_id,
            "deleted_at": datetime.utcnow().isoformat()
        }
    
    raise HTTPException(status_code=403, detail="Access denied") 