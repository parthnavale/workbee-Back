from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.notification import Notification
from schemas.notification_schemas import NotificationCreate, NotificationResponse, NotificationMarkRead
from datetime import datetime
from fastapi import APIRouter
from api.notification_ws import send_notification_to_worker
import asyncio

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/{worker_id}", response_model=List[NotificationResponse])
def get_notifications(worker_id: int, db: Session = Depends(get_db)):
    notifications = db.query(Notification).filter(Notification.worker_id == worker_id).order_by(Notification.created_at.desc()).all()
    return notifications

@router.post("/", response_model=NotificationResponse)
def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    db_notification = Notification(
        worker_id=notification.worker_id,
        job_id=notification.job_id,
        message=notification.message,
        is_read=False,
        created_at=datetime.utcnow()
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.post("/mark_read")
def mark_notifications_read(payload: NotificationMarkRead, db: Session = Depends(get_db)):
    updated = db.query(Notification).filter(Notification.id.in_(payload.notification_ids)).update({Notification.is_read: True}, synchronize_session=False)
    db.commit()
    return {"updated": updated}

@router.post("/test_ws/{worker_id}")
async def test_ws_notification(worker_id: int, message: str = "Test notification!"):
    # Send a test notification to the worker via WebSocket
    asyncio.create_task(send_notification_to_worker(worker_id, message))
    return {"success": True, "message": f"Notification sent to worker {worker_id}"} 