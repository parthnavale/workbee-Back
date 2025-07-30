from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.business_owner_schemas import BusinessOwnerCreate, BusinessOwnerUpdate, BusinessOwnerResponse, FCMTokenUpdate
from core.database import get_db
from models.business_owner import BusinessOwner
from models.user import User
from models.job import Job
from models.job_application import JobApplication
from datetime import datetime
from api.auth import require_business_owner, get_current_user

router = APIRouter(prefix="/business-owners", tags=["business_owners"])

@router.post("/", response_model=BusinessOwnerResponse)
def create_business_owner(
    owner: BusinessOwnerCreate, 
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    # Ensure user can only create business owner profile for themselves
    if owner.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only create a business owner profile for yourself"
        )
    
    # Check if user already has a business owner profile
    existing_owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == current_user.id).first()
    if existing_owner:
        raise HTTPException(status_code=400, detail="You already have a business owner profile")
    
    try:
        db_owner = BusinessOwner(**owner.dict())
        db.add(db_owner)
        db.commit()
        db.refresh(db_owner)
        return db_owner
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.get("/my-profile", response_model=BusinessOwnerResponse)
def get_my_business_profile(
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    """Get current user's business owner profile"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner profile not found")
    return owner

@router.get("/{owner_id}", response_model=BusinessOwnerResponse)
def get_business_owner(
    owner_id: int, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get business owner by ID (only if you own it or are admin)"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    
    # Only allow access if user owns this profile or is admin
    if owner.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return owner

@router.get("/", response_model=list[BusinessOwnerResponse])
def get_all_business_owners(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all business owners (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(BusinessOwner).all()

@router.put("/my-profile", response_model=BusinessOwnerResponse)
def update_my_business_profile(
    owner_update: BusinessOwnerUpdate,
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    """Update current user's business owner profile"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner profile not found")
    
    try:
        for key, value in owner_update.dict(exclude_unset=True).items():
            setattr(owner, key, value)
        db.commit()
        db.refresh(owner)
        return owner
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.put("/{owner_id}", response_model=BusinessOwnerResponse)
def update_business_owner(
    owner_id: int, 
    owner_update: BusinessOwnerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update business owner by ID (only if you own it or are admin)"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    
    # Only allow access if user owns this profile or is admin
    if owner.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        for key, value in owner_update.dict(exclude_unset=True).items():
            setattr(owner, key, value)
        db.commit()
        db.refresh(owner)
        return owner
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.delete("/my-profile")
def delete_my_business_profile(
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    """Delete current user's business owner profile and all associated data"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner profile not found")
    
    # Get all jobs by this business owner
    jobs = db.query(Job).filter(Job.business_owner_id == owner.id).all()
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
        "message": "Business owner profile and all associated data deleted successfully",
        "deleted_business_owner_id": owner.id,
        "deleted_jobs_count": len(jobs),
        "deleted_applications_count": len(applications),
        "deleted_at": datetime.utcnow().isoformat()
    }

@router.delete("/{owner_id}")
def delete_business_owner(
    owner_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete business owner by ID (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
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

@router.put("/my-profile/fcm-token")
def update_my_fcm_token(
    token_update: FCMTokenUpdate,
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    """Update current user's FCM token"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner profile not found")
    
    owner.fcm_token = token_update.fcm_token
    db.commit()
    return {"success": True, "fcm_token": owner.fcm_token}

@router.get("/my-profile/fcm-token")
def get_my_fcm_token(
    current_user: User = Depends(require_business_owner()),
    db: Session = Depends(get_db)
):
    """Get current user's FCM token"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == current_user.id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner profile not found")
    return {"fcm_token": owner.fcm_token}

@router.put("/{owner_id}/fcm-token")
def update_fcm_token(
    owner_id: int, 
    token_update: FCMTokenUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update FCM token by owner ID (only if you own it or are admin)"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    
    # Only allow access if user owns this profile or is admin
    if owner.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    owner.fcm_token = token_update.fcm_token
    db.commit()
    return {"success": True, "fcm_token": owner.fcm_token}

@router.get("/{owner_id}/fcm-token")
def get_fcm_token(
    owner_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get FCM token by owner ID (only if you own it or are admin)"""
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    
    # Only allow access if user owns this profile or is admin
    if owner.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {"fcm_token": owner.fcm_token} 