from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.worker_schemas import WorkerCreate, WorkerResponse
from core.database import get_db
from models.worker import Worker

router = APIRouter(prefix="/workers", tags=["workers"])

@router.post("/", response_model=WorkerResponse)
def create_worker(worker: WorkerCreate, db: Session = Depends(get_db)):
    db_worker = Worker(**worker.dict())
    db.add(db_worker)
    db.commit()
    db.refresh(db_worker)
    return db_worker

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
def update_worker(worker_id: int, worker_update: WorkerCreate, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    for key, value in worker_update.dict(exclude_unset=True).items():
        setattr(worker, key, value)
    db.commit()
    db.refresh(worker)
    return worker

@router.delete("/{worker_id}")
def delete_worker(worker_id: int, db: Session = Depends(get_db)):
    worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    db.delete(worker)
    db.commit()
    return {"detail": "Worker deleted"} 