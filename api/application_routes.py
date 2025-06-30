from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.job_application_schemas import JobApplicationCreate, JobApplicationResponse
from core.database import get_db
from models.job_application import JobApplication

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=JobApplicationResponse)
def apply_for_job(application: JobApplicationCreate, db: Session = Depends(get_db)):
    db_app = JobApplication(**application.dict())
    db.add(db_app)
    db.commit()
    db.refresh(db_app)
    return db_app

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
    return db.query(JobApplication).filter(JobApplication.job_id == job_id).all()

@router.get("/worker/{worker_id}", response_model=list[JobApplicationResponse])
def get_applications_by_worker(worker_id: int, db: Session = Depends(get_db)):
    return db.query(JobApplication).filter(JobApplication.worker_id == worker_id).all()

@router.put("/{application_id}", response_model=JobApplicationResponse)
def update_application(application_id: int, application_update: JobApplicationCreate, db: Session = Depends(get_db)):
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in application_update.dict(exclude_unset=True).items():
        setattr(app, key, value)
    db.commit()
    db.refresh(app)
    return app

@router.delete("/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    app = db.query(JobApplication).filter(JobApplication.id == application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(app)
    db.commit()
    return {"detail": "Application deleted"} 