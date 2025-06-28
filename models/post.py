"""
Post model module
Handles social media posts and content
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import Base

class Post(Base):
    """
    Post model for social media content
    Follows Single Responsibility Principle - only handles post data
    """
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, index=True)
    business_owner_id = Column(Integer, ForeignKey('business_owners.id'), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    media_urls = Column(JSON)  # Store media URLs as JSON array
    tags = Column(JSON)  # Store tags as JSON array
    likes_count = Column(Integer, default=0)
    shares_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    business_owner = relationship("BusinessOwner", back_populates="posts")
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}')>"
    
    @property
    def engagement_score(self) -> int:
        """Calculate engagement score based on likes and shares"""
        return self.likes_count + (self.shares_count * 2)
    
    @property
    def is_recent(self) -> bool:
        """Check if post is recent (within last 7 days)"""
        return (datetime.utcnow() - self.created_at).days <= 7 