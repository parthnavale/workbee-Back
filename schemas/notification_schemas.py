from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    worker_id: int
    job_id: int
    message: str

class NotificationCreate(NotificationBase):
    pass

class NotificationResponse(NotificationBase):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NotificationMarkRead(BaseModel):
    notification_ids: list[int] 