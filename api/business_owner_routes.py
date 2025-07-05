from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.business_owner_schemas import BusinessOwnerCreate, BusinessOwnerUpdate, BusinessOwnerResponse
from core.database import get_db
from models.business_owner import BusinessOwner
from models.user import User
from models.job import Job
from models.job_application import JobApplication
from datetime import datetime

router = APIRouter(prefix="/business-owners", tags=["business_owners"])

@router.post("/", response_model=BusinessOwnerResponse)
def create_business_owner(owner: BusinessOwnerCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == owner.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail=f"User with id {owner.user_id} not found")
    
    # Check if user already has a business owner profile
    existing_owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == owner.user_id).first()
    if existing_owner:
        raise HTTPException(status_code=400, detail=f"User {owner.user_id} already has a business owner profile")
    
    try:
        db_owner = BusinessOwner(**owner.dict())
        db.add(db_owner)
        db.commit()
        db.refresh(db_owner)
        return db_owner
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.get("/{owner_id}", response_model=BusinessOwnerResponse)
def get_business_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    return owner

@router.get("/", response_model=list[BusinessOwnerResponse])
def get_all_business_owners(db: Session = Depends(get_db)):
    return db.query(BusinessOwner).all()

@router.put("/{owner_id}", response_model=BusinessOwnerResponse)
def update_business_owner(owner_id: int, owner_update: BusinessOwnerUpdate, db: Session = Depends(get_db)):
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    
    try:
        for key, value in owner_update.dict(exclude_unset=True).items():
            setattr(owner, key, value)
        db.commit()
        db.refresh(owner)
        return owner
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.delete("/{owner_id}")
def delete_business_owner(owner_id: int, db: Session = Depends(get_db)):
    """Delete business owner and all associated jobs and applications"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    
    # Get all jobs by this business owner
    jobs = db.query(Job).filter(Job.business_owner_id == owner_id).all()
    job_ids = [job.id for job in jobs]
    
    # Get all applications for these jobs
    applications = []
    if job_ids:
        applications = db.query(JobApplication).filter(JobApplication.job_id.in_(job_ids)).all()
    
    # Delete applications first (due to foreign key constraints)
    for application in applications:
        db.delete(application)
    
    # Delete jobs
    for job in jobs:
        db.delete(job)
    
    # Delete business owner
    db.delete(owner)
    db.commit()
    
    return {
        "success": True,
        "message": "Business owner and all associated data deleted successfully",
        "deleted_business_owner_id": owner_id,
        "deleted_jobs_count": len(jobs),
        "deleted_applications_count": len(applications),
        "deleted_at": datetime.utcnow().isoformat()
    } 