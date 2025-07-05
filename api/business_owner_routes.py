from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.business_owner_schemas import BusinessOwnerCreate, BusinessOwnerUpdate, BusinessOwnerResponse
from core.database import get_db
from models.business_owner import BusinessOwner

router = APIRouter(prefix="/business-owners", tags=["business_owners"])

@router.post("/", response_model=BusinessOwnerResponse)
def create_business_owner(owner: BusinessOwnerCreate, db: Session = Depends(get_db)):
    db_owner = BusinessOwner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

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
    for key, value in owner_update.dict(exclude_unset=True).items():
        setattr(owner, key, value)
    db.commit()
    db.refresh(owner)
    return owner

@router.delete("/{owner_id}")
def delete_business_owner(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(BusinessOwner).filter(BusinessOwner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Business owner not found")
    db.delete(owner)
    db.commit()
    return {"detail": "Business owner deleted"} 