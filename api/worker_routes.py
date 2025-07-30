from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.worker_schemas import WorkerCreate, WorkerUpdate, WorkerResponse
from core.database import get_db
from models.worker import Worker
from models.user import User
from models.job_application import JobApplication
from datetime import datetime
from api.auth import require_worker, get_current_user

router = APIRouter(prefix="/workers", tags=["workers"])

@router.post("/", response_model=WorkerResponse)
def create_worker(
    worker: WorkerCreate,
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    # Ensure user can only create worker profile for themselves
    if worker.user_id != current_user.id:
        raise HTTPException(
            status_code=403, 
            detail="You can only create a worker profile for yourself"
        )
    
    # Check if user already has a worker profile
    existing_worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if existing_worker:
        raise HTTPException(status_code=400, detail="You already have a worker profile")
    
    try:
        db_worker = Worker(
            user_id=worker.user_id,
            name=worker.name,
            phone=worker.phone,
            email=worker.email,
            skills=worker.skills,
            years_of_experience=worker.years_of_experience,
            address=worker.address,
            state=worker.state,
            city=worker.city,
            pincode=worker.pincode,
            latitude=worker.latitude,
            longitude=worker.longitude,
            fcm_token=worker.fcm_token
        )
        db.add(db_worker)
        db.commit()
        db.refresh(db_worker)
        return db_worker
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.get("/my-profile", response_model=WorkerResponse)
def get_my_worker_profile(
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    """Get current user's worker profile"""
    worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker profile not found")
    return worker

@router.get("/{worker_id}", response_model=WorkerResponse)
def get_worker(
    worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get worker by ID (only if you own it or are admin)"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Only allow access if user owns this profile or is admin
    if worker.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return worker

@router.get("/", response_model=list[WorkerResponse])
def get_all_workers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all workers (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(Worker).all()

@router.put("/my-profile", response_model=WorkerResponse)
def update_my_worker_profile(
    worker_update: WorkerUpdate,
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    """Update current user's worker profile"""
    worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker profile not found")
    
    try:
        for key, value in worker_update.dict(exclude_unset=True).items():
            setattr(worker, key, value)
        db.commit()
        db.refresh(worker)
        return worker
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.put("/{worker_id}", response_model=WorkerResponse)
def update_worker(
    worker_id: int,
    worker_update: WorkerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update worker by ID (only if you own it or are admin)"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Only allow access if user owns this profile or is admin
    if worker.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        for key, value in worker_update.dict(exclude_unset=True).items():
            setattr(worker, key, value)
        db.commit()
        db.refresh(worker)
        return worker
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.put("/my-profile/fcm-token")
def update_my_fcm_token(
    fcm_token: str,
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    """Update current user's FCM token"""
    worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker profile not found")
    
    worker.fcm_token = fcm_token
    db.commit()
    db.refresh(worker)
    return {"success": True, "worker_id": worker.id, "fcm_token": fcm_token}

@router.get("/my-profile/fcm-token")
def get_my_fcm_token(
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    """Get current user's FCM token"""
    worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker profile not found")
    return {"worker_id": worker.id, "fcm_token": worker.fcm_token}

@router.put("/{worker_id}/fcm-token")
def update_fcm_token(
    worker_id: int,
    fcm_token: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update FCM token by worker ID (only if you own it or are admin)"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Only allow access if user owns this profile or is admin
    if worker.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    worker.fcm_token = fcm_token
    db.commit()
    db.refresh(worker)
    return {"success": True, "worker_id": worker_id, "fcm_token": fcm_token}

@router.get("/{worker_id}/fcm-token")
def get_worker_fcm_token(
    worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get FCM token by worker ID (only if you own it or are admin)"""
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Only allow access if user owns this profile or is admin
    if worker.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {"worker_id": worker_id, "fcm_token": worker.fcm_token}

@router.post("/test-fcm")
def test_fcm_notification(
    request: dict,
    current_user: User = Depends(require_worker())
):
    """Test endpoint to send FCM notification (worker only)"""
    try:
        from core.fcm import send_fcm_notification
        token = request.get("token")
        title = request.get("title", "Test Notification")
        body = request.get("body", "Test message")
        
        if not token:
            raise HTTPException(status_code=400, detail="FCM token is required")
        
        send_fcm_notification(token, title, body)
        return {"success": True, "message": "Test notification sent"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

@router.delete("/my-profile")
def delete_my_worker_profile(
    current_user: User = Depends(require_worker()),
    db: Session = Depends(get_db)
):
    """Delete current user's worker profile and all associated data"""
    worker = db.query(Worker).filter(Worker.user_id == current_user.id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker profile not found")
    
    # Get all applications by this worker
    applications = db.query(JobApplication).filter(JobApplication.worker_id == worker.id).all()
    
    # Delete applications first (due to foreign key constraints)
    for application in applications:
        db.delete(application)
    
    # Delete worker
    db.delete(worker)
    db.commit()
    
    return {
        "success": True,
        "message": "Worker profile and all associated data deleted successfully",
        "deleted_worker_id": worker.id,
        "deleted_applications_count": len(applications),
        "deleted_at": datetime.utcnow().isoformat()
    }

@router.delete("/{worker_id}")
def delete_worker(
    worker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete worker by ID (admin only)"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # Get all applications by this worker
    applications = db.query(JobApplication).filter(JobApplication.worker_id == worker_id).all()
    
    # Delete applications first (due to foreign key constraints)
    for application in applications:
        db.delete(application)
    
    # Delete worker
    db.delete(worker)
    db.commit()
    
    return {
        "success": True,
        "message": "Worker and all associated data deleted successfully",
        "deleted_worker_id": worker_id,
        "deleted_applications_count": len(applications),
        "deleted_at": datetime.utcnow().isoformat()
    } 