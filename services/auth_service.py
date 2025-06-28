"""
Authentication Service module
Handles user authentication and authorization
"""
import hashlib
import secrets
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from models.user import User
from repositories.user_repository import UserRepository
from schemas.user_schemas import UserCreate, UserLogin

class AuthService:
    """
    Authentication Service for user authentication and authorization
    Follows Service Layer pattern and Strategy pattern
    """
    
    def __init__(self):
        """Initialize with user repository"""
        self.user_repository = UserRepository()
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256
        Args:
            password: Plain text password
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against hash
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password
        Returns:
            True if password matches, False otherwise
        """
        return self.hash_password(plain_password) == hashed_password
    
    def generate_token(self) -> str:
        """
        Generate random token for authentication
        Returns:
            Random token string
        """
        return secrets.token_urlsafe(32)
    
    def register_user(self, db: Session, user_data: UserCreate) -> Tuple[bool, str, Optional[User]]:
        """
        Register new user
        Args:
            db: Database session
            user_data: User creation data
        Returns:
            Tuple of (success, message, user_instance)
        """
        # Check if username exists
        if self.user_repository.username_exists(db, user_data.username):
            return False, "Username already exists", None
        
        # Check if email exists
        if self.user_repository.email_exists(db, user_data.email):
            return False, "Email already exists", None
        
        # Hash password
        hashed_password = self.hash_password(user_data.password)
        
        # Create user
        user_dict = user_data.dict()
        user_dict['password_hash'] = hashed_password
        del user_dict['password']
        
        try:
            user = self.user_repository.create(db, user_dict)
            return True, "User registered successfully", user
        except Exception as e:
            return False, f"Registration failed: {str(e)}", None
    
    def authenticate_user(self, db: Session, login_data: UserLogin) -> Tuple[bool, str, Optional[User]]:
        """
        Authenticate user login
        Args:
            db: Database session
            login_data: Login credentials
        Returns:
            Tuple of (success, message, user_instance)
        """
        # Get user by username
        user = self.user_repository.get_by_username(db, login_data.username)
        
        if not user:
            return False, "Invalid username or password", None
        
        # Check if user is active
        if not user.is_active:
            return False, "Account is deactivated", None
        
        # Verify password
        if not self.verify_password(login_data.password, user.password_hash):
            return False, "Invalid username or password", None
        
        return True, "Authentication successful", user
    
    def change_password(self, db: Session, user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password
        Args:
            db: Database session
            user_id: User ID
            old_password: Current password
            new_password: New password
        Returns:
            Tuple of (success, message)
        """
        # Get user
        user = self.user_repository.get(db, user_id)
        if not user:
            return False, "User not found"
        
        # Verify old password
        if not self.verify_password(old_password, user.password_hash):
            return False, "Current password is incorrect"
        
        # Hash new password
        new_hashed_password = self.hash_password(new_password)
        
        # Update password
        try:
            self.user_repository.update(db, user, {"password_hash": new_hashed_password})
            return True, "Password changed successfully"
        except Exception as e:
            return False, f"Password change failed: {str(e)}"
    
    def deactivate_user(self, db: Session, user_id: int) -> Tuple[bool, str]:
        """
        Deactivate user account
        Args:
            db: Database session
            user_id: User ID
        Returns:
            Tuple of (success, message)
        """
        user = self.user_repository.get(db, user_id)
        if not user:
            return False, "User not found"
        
        try:
            self.user_repository.update(db, user, {"is_active": False})
            return True, "User deactivated successfully"
        except Exception as e:
            return False, f"Deactivation failed: {str(e)}"
    
    def activate_user(self, db: Session, user_id: int) -> Tuple[bool, str]:
        """
        Activate user account
        Args:
            db: Database session
            user_id: User ID
        Returns:
            Tuple of (success, message)
        """
        user = self.user_repository.get(db, user_id)
        if not user:
            return False, "User not found"
        
        try:
            self.user_repository.update(db, user, {"is_active": True})
            return True, "User activated successfully"
        except Exception as e:
            return False, f"Activation failed: {str(e)}" 