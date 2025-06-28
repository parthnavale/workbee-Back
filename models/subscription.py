"""
Subscription model module
Handles subscription and billing data
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from core.database import Base

class SubscriptionType(str, enum.Enum):
    """Subscription type enumeration"""
    BASIC = "basic"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(str, enum.Enum):
    """Subscription status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class Subscription(Base):
    """
    Subscription model for managing business subscriptions
    Follows Single Responsibility Principle - only handles subscription data
    """
    __tablename__ = 'subscriptions'
    
    id = Column(Integer, primary_key=True, index=True)
    business_owner_id = Column(Integer, ForeignKey('business_owners.id'), unique=True, nullable=False)
    subscription_type = Column(Enum(SubscriptionType), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    auto_renew = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships - following Open/Closed Principle
    business_owner = relationship("BusinessOwner", back_populates="subscription")
    
    def __repr__(self):
        return f"<Subscription(id={self.id}, type='{self.subscription_type}', status='{self.status}')>"
    
    @property
    def is_active(self) -> bool:
        """Check if subscription is active"""
        return self.status == SubscriptionStatus.ACTIVE and datetime.utcnow() <= self.end_date
    
    @property
    def is_expired(self) -> bool:
        """Check if subscription is expired"""
        return datetime.utcnow() > self.end_date
    
    @property
    def days_remaining(self) -> int:
        """Get days remaining in subscription"""
        if self.is_expired:
            return 0
        return (self.end_date - datetime.utcnow()).days 