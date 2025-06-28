"""
Base Repository module
Implements the Repository pattern with common CRUD operations
"""
from typing import Generic, TypeVar, Type, Optional, List, Any, Dict
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Base Repository class implementing common CRUD operations
    Follows Repository pattern and Template Method pattern
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize repository with model class
        Args:
            model: SQLAlchemy model class
        """
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """
        Get entity by ID
        Args:
            db: Database session
            id: Entity ID
        Returns:
            Entity instance or None
        """
        return db.query(self.model).filter(self.model.id == id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """
        Get multiple entities with pagination and filtering
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of filters to apply
        Returns:
            List of entities
        """
        query = db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, obj_in: Dict[str, Any]) -> ModelType:
        """
        Create new entity
        Args:
            db: Database session
            obj_in: Dictionary with entity data
        Returns:
            Created entity instance
        """
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update(
        self, 
        db: Session, 
        db_obj: ModelType, 
        obj_in: Dict[str, Any]
    ) -> ModelType:
        """
        Update existing entity
        Args:
            db: Database session
            db_obj: Existing entity instance
            obj_in: Dictionary with update data
        Returns:
            Updated entity instance
        """
        for field, value in obj_in.items():
            if hasattr(db_obj, field) and value is not None:
                setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def delete(self, db: Session, id: int) -> bool:
        """
        Delete entity by ID
        Args:
            db: Database session
            id: Entity ID
        Returns:
            True if deleted, False if not found
        """
        obj = db.query(self.model).get(id)
        if obj:
            db.delete(obj)
            db.commit()
            return True
        return False
    
    def exists(self, db: Session, id: int) -> bool:
        """
        Check if entity exists
        Args:
            db: Database session
            id: Entity ID
        Returns:
            True if exists, False otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first() is not None
    
    def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """
        Count entities with optional filters
        Args:
            db: Database session
            filters: Dictionary of filters to apply
        Returns:
            Count of entities
        """
        query = db.query(self.model)
        
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key) and value is not None:
                    query = query.filter(getattr(self.model, key) == value)
        
        return query.count() 