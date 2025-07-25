from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from schemas.worker_schemas import WorkerCreate, WorkerUpdate, WorkerResponse
from core.database import get_db
from models.worker import Worker
from models.user import User
from models.job_application import JobApplication
from datetime import datetime

router = APIRouter(prefix="/workers", tags=["workers"])

@router.post("/", response_model=WorkerResponse)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user = db.query(User).filter(User.id == worker.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail=f"User with id {worker.user_id} not found")
    
    # Check if user already has a worker profile
    existing_worker = db.query(Worker).filter(Worker.user_id == worker.user_id).first()
    if existing_worker:
        raise HTTPException(status_code=400, detail=f"User {worker.user_id} already has a worker profile")
    
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

@router.get("/{worker_id}", response_model=WorkerResponse)
def get_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.get("/", response_model=list[WorkerResponse])
def get_all_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()

@router.put("/{worker_id}", response_model=WorkerResponse)
def update_worker(worker_id: int, worker_update: WorkerUpdate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    try:
        for key, value in worker_update.dict(exclude_unset=True).items():
            setattr(worker, key, value)
        db.commit()
        db.refresh(worker)
        return worker
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Invalid data provided")

@router.put("/{worker_id}/fcm-token")
def update_fcm_token(worker_id: int, fcm_token: str, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    worker.fcm_token = fcm_token
    db.commit()
    db.refresh(worker)
    return {"success": True, "worker_id": worker_id, "fcm_token": fcm_token}

@router.get("/{worker_id}/fcm-token")
def get_worker_fcm_token(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return {"worker_id": worker_id, "fcm_token": worker.fcm_token}

@router.post("/test-fcm")
def test_fcm_notification(request: dict):
    """Test endpoint to send FCM notification"""
    try:
        from core.fcm import send_fcm_notification
        token = request.get("token")
        title = request.get("title", "Test Notification")
        body = request.get("body", "Test message")
        data = request.get("data", {})
        
        if not token:
            raise HTTPException(status_code=400, detail="FCM token is required")
            
        result = send_fcm_notification(token, title, body, data)
        return {"success": True, "message": "FCM notification sent", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send FCM notification: {str(e)}")

@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    """Delete worker and all associated job applications"""
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
        "message": "Worker and all associated applications deleted successfully",
        "deleted_worker_id": worker_id,
        "deleted_applications_count": len(applications),
        "deleted_at": datetime.utcnow().isoformat()
    } 