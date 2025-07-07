import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from schemas.user_schemas import UserCreate, UserUpdate, UserLogin, UserResponse
from schemas.business_owner_schemas import BusinessOwnerCreate
from core.database import get_db
from models.user import User
from models.business_owner import BusinessOwner
from models.worker import Worker
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["users"])

# Load the JWT secret from environment variable
SECRET_KEY = os.environ.get("WORKBEE_SECRET_KEY", "workbee_secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "id": db_user.id,
        "username": db_user.username,
        "role": db_user.role
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    users = db.query(User).all()
    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    """Update a user"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if email is already taken by another user
    if user_update.email and user_update.email != db_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Update user fields
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = str(user_update.email)
    if user_update.role is not None:
        db_user.role = user_update.role
    if user_update.password is not None:
        db_user.password_hash = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete a user and all associated data"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check for associated data
    business_owner = db.query(BusinessOwner).filter(BusinessOwner.user_id == user_id).first()
    worker = db.query(Worker).filter(Worker.user_id == user_id).first()
    
    if business_owner or worker:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete user with associated data. User has business_owner_id={business_owner.id if business_owner else None}, worker_id={worker.id if worker else None}. Delete the associated profile first."
        )
    
    # Delete the user
    db.delete(user)
    db.commit()
    
    return {
        "success": True,
        "message": "User deleted successfully",
        "deleted_user_id": user_id,
        "deleted_at": datetime.utcnow().isoformat()
    }

@router.post("/register-business-owner", response_model=UserResponse)
def register_business_owner(
    user: UserCreate,
    business_owner: BusinessOwnerCreate,
    db: Session = Depends(get_db)
):
    try:
        # Check if user already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, email=user.email, password_hash=hashed_password, role="poster")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        # Create business owner profile
        new_owner = BusinessOwner(
            user_id=new_user.id,
            business_name=business_owner.business_name,
            contact_person=business_owner.contact_person,
            contact_phone=business_owner.contact_phone,
            contact_email=business_owner.contact_email,
            address=business_owner.address,
            website=business_owner.website,
            industry=business_owner.industry,
            state=business_owner.state,
            city=business_owner.city,
            pincode=business_owner.pincode,
            year_established=business_owner.year_established
        )
        db.add(new_owner)
        db.commit()
        db.refresh(new_owner)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {e}") 