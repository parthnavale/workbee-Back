"""
User Repository module
Implements user-specific database operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from models.user import User, UserRole
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """
    User Repository for user-specific operations
    Follows Repository pattern and inherits from BaseRepository
    """
    
    def __init__(self):
        """Initialize with User model"""
        super().__init__(User)
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Get user by username
        Args:
            db: Database session
            username: Username to search for
        Returns:
            User instance or None
        """
        return db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        Args:
            db: Database session
            email: Email to search for
        Returns:
            User instance or None
        """
        return db.query(User).filter(User.email == email).first()
    
    def get_by_role(self, db: Session, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get users by role
        Args:
            db: Database session
            role: User role to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
        Returns:
            List of users with specified role
        """
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def get_active_users(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Get active users
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
        Returns:
            List of active users
        """
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()
    
    def authenticate_user(self, db: Session, username: str, password_hash: str) -> Optional[User]:
        """
        Authenticate user with username and password hash
        Args:
            db: Database session
            username: Username
            password_hash: Hashed password
        Returns:
            User instance if authenticated, None otherwise
        """
        return db.query(User).filter(
            and_(
                User.username == username,
                User.password_hash == password_hash,
                User.is_active == True
            )
        ).first()
    
    def username_exists(self, db: Session, username: str) -> bool:
        """
        Check if username exists
        Args:
            db: Database session
            username: Username to check
        Returns:
            True if exists, False otherwise
        """
        return db.query(User).filter(User.username == username).first() is not None
    
    def email_exists(self, db: Session, email: str) -> bool:
        """
        Check if email exists
        Args:
            db: Database session
            email: Email to check
        Returns:
            True if exists, False otherwise
        """
        return db.query(User).filter(User.email == email).first() is not None 