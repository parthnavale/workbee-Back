#!/usr/bin/env python3
"""
Script to create all database tables for the Workbee application.
Run this script to set up your database schema.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import engine, Base
from models.user import User
from models.business_owner import BusinessOwner
from models.worker import Worker
from models.job import Job
from models.job_application import JobApplication

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # List created tables
        print("\nCreated tables:")
        for table in Base.metadata.tables:
            print(f"  - {table}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Workbee Database Setup")
    print("=" * 30)
    
    if create_tables():
        print("\n🎉 Database setup completed successfully!")
        print("You can now run your FastAPI application.")
    else:
        print("\n💥 Database setup failed!")
        sys.exit(1) 