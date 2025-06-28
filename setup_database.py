#!/usr/bin/env python3
"""
Database setup script for WorkShift API
This script will create the database tables and add some sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal
import models
from datetime import datetime
import json

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def add_sample_data():
    """Add sample data to the database"""
    print("Adding sample data...")
    db = SessionLocal()
    
    try:
        # Create sample users
        user1 = models.User(
            username="business_owner1",
            email="owner1@example.com",
            password_hash="password123",  # In production, use proper hashing
            role="business_owner"
        )
        user2 = models.User(
            username="worker1",
            email="worker1@example.com",
            password_hash="password123",
            role="worker"
        )
        
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        
        # Create sample business owner
        business_owner = models.BusinessOwner(
            user_id=user1.id,
            business_name="ABC Retail Store",
            business_registration_number="BRN001",
            contact_person="John Doe",
            contact_phone="9876543210",
            contact_email="john@abcretail.com",
            type_of_business="Retail",
            year_established=2020,
            state="Maharashtra",
            city="Mumbai",
            pincode="400001",
            address="123 Main Street, Mumbai, Maharashtra"
        )
        
        # Create sample worker
        worker = models.Worker(
            user_id=user2.id,
            name="Jane Smith",
            phone="9876543211",
            email="jane@example.com",
            skills=json.dumps(["Cashier", "Customer Service", "Inventory Management"]),
            years_of_experience=3,
            previous_work_experience="Worked at XYZ Supermarket for 2 years",
            state="Maharashtra",
            city="Mumbai",
            pincode="400002",
            address="456 Park Avenue, Mumbai, Maharashtra"
        )
        
        db.add(business_owner)
        db.add(worker)
        db.commit()
        db.refresh(business_owner)
        db.refresh(worker)
        
        # Create sample jobs
        job1 = models.Job(
            business_owner_id=business_owner.id,
            title="Cashier",
            description="Looking for an experienced cashier for our retail store. Must be good with customers and have basic math skills.",
            required_skills=json.dumps(["Cashier", "Customer Service"]),
            location="Mumbai",
            address="123 Main Street, Mumbai, Maharashtra",
            state="Maharashtra",
            city="Mumbai",
            pincode="400001",
            hourly_rate=150.0,
            estimated_hours=8,
            posted_date=datetime.now(),
            contact_person="John Doe",
            contact_phone="9876543210",
            contact_email="john@abcretail.com"
        )
        
        job2 = models.Job(
            business_owner_id=business_owner.id,
            title="Store Associate",
            description="Need a store associate to help with inventory management and customer service.",
            required_skills=json.dumps(["Store Associate", "Inventory Management", "Customer Service"]),
            location="Mumbai",
            address="123 Main Street, Mumbai, Maharashtra",
            state="Maharashtra",
            city="Mumbai",
            pincode="400001",
            hourly_rate=180.0,
            estimated_hours=6,
            posted_date=datetime.now(),
            contact_person="John Doe",
            contact_phone="9876543210",
            contact_email="john@abcretail.com"
        )
        
        db.add(job1)
        db.add(job2)
        db.commit()
        
        print("✅ Sample data added successfully!")
        print(f"Created {db.query(models.User).count()} users")
        print(f"Created {db.query(models.BusinessOwner).count()} business owners")
        print(f"Created {db.query(models.Worker).count()} workers")
        print(f"Created {db.query(models.Job).count()} jobs")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to set up the database"""
    print("🚀 Setting up WorkShift Database...")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
    # Add sample data
    add_sample_data()
    
    print("=" * 50)
    print("🎉 Database setup completed!")
    print("\nYou can now start the API server with:")
    print("python main.py")
    print("\nOr with uvicorn:")
    print("uvicorn main:app --reload --host 0.0.0.0 --port 8000")

if __name__ == "__main__":
    main() 