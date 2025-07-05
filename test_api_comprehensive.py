#!/usr/bin/env python3
"""
Comprehensive API Test Script for Workbee Backend
Tests all CRUD operations for all entities:
- Users (Register, Login, Get)
- Business Owners (Create, Read, Update, Delete)
- Workers (Create, Read, Update, Delete)
- Jobs (Create, Read, Update, Delete)
- Job Applications (Create, Read, Update, Delete)
- JWT Authentication
"""

import requests
import json
import time

BASE_URL = "https://myworkbee.duckdns.org"

# Test data storage
test_data = {
    'user_ids': [],
    'business_owner_ids': [],
    'worker_ids': [],
    'job_ids': [],
    'application_ids': [],
    'tokens': {}
}

def print_result(name, resp, expected_status=200):
    """Print test results with color coding"""
    print(f"\n{'='*50}")
    print(f"🧪 {name}")
    print(f"{'='*50}")
    print(f"Status: {resp.status_code} {'✅' if resp.status_code == expected_status else '❌'}")
    print(f"URL: {resp.url}")
    
    try:
        if resp.text:
            if resp.headers.get('content-type', '').startswith('application/json'):
                print("Response:")
                print(json.dumps(resp.json(), indent=2))
            else:
                print(f"Response: {resp.text}")
        else:
            print("Response: Empty")
    except Exception as e:
        print(f"Response: {resp.text}")
        print(f"Error parsing JSON: {e}")

def test_jwt_authentication():
    """Test JWT authentication endpoints"""
    print("\n🔐 TESTING JWT AUTHENTICATION")
    
    # Test getting JWT token
    token_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    resp = requests.post(f"{BASE_URL}/api/auth/token", data=token_data)
    print_result("Get JWT Token", resp)
    
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        test_data['tokens']['jwt'] = token
        headers = {"Authorization": f"Bearer {token}"}
        
        # Test protected endpoint
        resp = requests.get(f"{BASE_URL}/api/auth/protected", headers=headers)
        print_result("Test Protected Endpoint", resp)
    else:
        print("❌ Failed to get JWT token")

def test_user_operations():
    """Test user registration and login"""
    print("\n👤 TESTING USER OPERATIONS")
    
    # Test user registration (Business Owner)
    user_data = {
        "username": "business_owner_test",
        "email": "business_owner_test@example.com",
        "password": "password123",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    print_result("Register Business Owner User", resp)
    
    if resp.status_code == 200:
        user_id = resp.json().get("id")
        test_data['user_ids'].append(user_id)
        print(f"✅ Created user with ID: {user_id}")
    else:
        print("❌ Failed to create business owner user")
        return False
    
    # Test user registration (Worker)
    worker_user_data = {
        "username": "worker_test",
        "email": "worker_test@example.com",
        "password": "password123",
        "role": "seeker"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=worker_user_data)
    print_result("Register Worker User", resp)
    
    if resp.status_code == 200:
        user_id = resp.json().get("id")
        test_data['user_ids'].append(user_id)
        print(f"✅ Created worker user with ID: {user_id}")
    else:
        print("❌ Failed to create worker user")
        return False
    
    # Test user login
    login_data = {
        "email": "business_owner_test@example.com",
        "password": "password123"
    }
    resp = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print_result("User Login", resp)
    
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        test_data['tokens']['user'] = token
        print(f"✅ Got user token")
    
    return True

def test_business_owner_operations():
    """Test business owner CRUD operations"""
    print("\n🏢 TESTING BUSINESS OWNER OPERATIONS")
    
    if not test_data['user_ids']:
        print("❌ No users available for business owner creation")
        return False
    
    user_id = test_data['user_ids'][0]
    
    # CREATE - Create business owner
    business_owner_data = {
        "user_id": user_id,
        "business_name": "Test Business Corp",
        "contact_person": "John Doe",
        "contact_phone": "1234567890",
        "contact_email": "john@testbusiness.com",
        "address": "123 Test Street",
        "website": "https://testbusiness.com",
        "industry": "Technology",
        "state": "CA",
        "city": "San Francisco",
        "pincode": "94105",
        "year_established": 2020
    }
    resp = requests.post(f"{BASE_URL}/business-owners/", json=business_owner_data)
    print_result("Create Business Owner", resp)
    
    if resp.status_code == 200:
        business_owner_id = resp.json().get("id")
        test_data['business_owner_ids'].append(business_owner_id)
        print(f"✅ Created business owner with ID: {business_owner_id}")
    else:
        print("❌ Failed to create business owner")
        return False
    
    # READ - Get all business owners
    resp = requests.get(f"{BASE_URL}/business-owners/")
    print_result("Get All Business Owners", resp)
    
    # READ - Get specific business owner
    resp = requests.get(f"{BASE_URL}/business-owners/{business_owner_id}")
    print_result("Get Specific Business Owner", resp)
    
    # UPDATE - Update business owner
    update_data = {
        "business_name": "Updated Test Business Corp",
        "contact_person": "Jane Doe",
        "contact_phone": "0987654321"
    }
    resp = requests.put(f"{BASE_URL}/business-owners/{business_owner_id}", json=update_data)
    print_result("Update Business Owner", resp, 200)
    
    # DELETE - Delete business owner
    resp = requests.delete(f"{BASE_URL}/business-owners/{business_owner_id}")
    print_result("Delete Business Owner", resp, 200)
    
    if resp.status_code == 200:
        test_data['business_owner_ids'].remove(business_owner_id)
        print(f"✅ Deleted business owner with ID: {business_owner_id}")
    
    return True

def test_worker_operations():
    """Test worker CRUD operations"""
    print("\n👷 TESTING WORKER OPERATIONS")
    
    if len(test_data['user_ids']) < 2:
        print("❌ Not enough users available for worker creation")
        return False
    
    user_id = test_data['user_ids'][1]  # Use the second user (worker)
    
    # CREATE - Create worker
    worker_data = {
        "user_id": user_id,
        "name": "Alice Worker",
        "phone": "5551234567",
        "email": "alice@worker.com",
        "skills": "Python,JavaScript,React",
        "years_of_experience": 3,
        "address": "456 Worker Street",
        "state": "CA",
        "city": "San Francisco",
        "pincode": "94107"
    }
    resp = requests.post(f"{BASE_URL}/workers/", json=worker_data)
    print_result("Create Worker", resp)
    
    if resp.status_code == 200:
        worker_id = resp.json().get("id")
        test_data['worker_ids'].append(worker_id)
        print(f"✅ Created worker with ID: {worker_id}")
    else:
        print("❌ Failed to create worker")
        return False
    
    # READ - Get all workers
    resp = requests.get(f"{BASE_URL}/workers/")
    print_result("Get All Workers", resp)
    
    # READ - Get specific worker
    resp = requests.get(f"{BASE_URL}/workers/{worker_id}")
    print_result("Get Specific Worker", resp)
    
    # UPDATE - Update worker
    update_data = {
        "name": "Alice Updated Worker",
        "skills": "Python,JavaScript,React,Node.js",
        "years_of_experience": 4
    }
    resp = requests.put(f"{BASE_URL}/workers/{worker_id}", json=update_data)
    print_result("Update Worker", resp, 200)
    
    # DELETE - Delete worker
    resp = requests.delete(f"{BASE_URL}/workers/{worker_id}")
    print_result("Delete Worker", resp, 200)
    
    if resp.status_code == 200:
        test_data['worker_ids'].remove(worker_id)
        print(f"✅ Deleted worker with ID: {worker_id}")
    
    return True

def test_job_operations():
    """Test job CRUD operations"""
    print("\n💼 TESTING JOB OPERATIONS")
    
    # Create a business owner first if needed
    if not test_data['business_owner_ids']:
        print("Creating a business owner for job testing...")
        if not test_business_owner_operations():
            print("❌ Failed to create business owner for job testing")
            return False
    
    business_owner_id = test_data['business_owner_ids'][0]
    
    # CREATE - Create job
    job_data = {
        "business_owner_id": business_owner_id,
        "title": "Senior Python Developer",
        "description": "We are looking for an experienced Python developer...",
        "required_skills": "Python,Django,FastAPI,PostgreSQL",
        "location": "San Francisco",
        "address": "123 Tech Street",
        "state": "CA",
        "city": "San Francisco",
        "pincode": "94105",
        "hourly_rate": 75.0,
        "estimated_hours": 40,
        "start_date": "2024-08-01T09:00:00",
        "contact_person": "HR Manager",
        "contact_phone": "1234567890",
        "contact_email": "hr@techcompany.com"
    }
    resp = requests.post(f"{BASE_URL}/jobs/", json=job_data)
    print_result("Create Job", resp)
    
    if resp.status_code == 200:
        job_id = resp.json().get("id")
        test_data['job_ids'].append(job_id)
        print(f"✅ Created job with ID: {job_id}")
    else:
        print("❌ Failed to create job")
        return False
    
    # READ - Get all jobs
    resp = requests.get(f"{BASE_URL}/jobs/")
    print_result("Get All Jobs", resp)
    
    # READ - Get specific job
    resp = requests.get(f"{BASE_URL}/jobs/{job_id}")
    print_result("Get Specific Job", resp)
    
    # UPDATE - Update job
    update_data = {
        "title": "Senior Full Stack Developer",
        "hourly_rate": 85.0,
        "required_skills": "Python,Django,FastAPI,React,PostgreSQL"
    }
    resp = requests.put(f"{BASE_URL}/jobs/{job_id}", json=update_data)
    print_result("Update Job", resp, 200)
    
    # DELETE - Delete job
    resp = requests.delete(f"{BASE_URL}/jobs/{job_id}")
    print_result("Delete Job", resp, 200)
    
    if resp.status_code == 200:
        test_data['job_ids'].remove(job_id)
        print(f"✅ Deleted job with ID: {job_id}")
    
    return True

def test_job_application_operations():
    """Test job application CRUD operations"""
    print("\n📝 TESTING JOB APPLICATION OPERATIONS")
    
    # Create a job and worker first if needed
    if not test_data['job_ids']:
        print("Creating a job for application testing...")
        if not test_job_operations():
            print("❌ Failed to create job for application testing")
            return False
    
    if not test_data['worker_ids']:
        print("Creating a worker for application testing...")
        if not test_worker_operations():
            print("❌ Failed to create worker for application testing")
            return False
    
    job_id = test_data['job_ids'][0]
    worker_id = test_data['worker_ids'][0]
    
    # CREATE - Create job application
    application_data = {
        "job_id": job_id,
        "worker_id": worker_id,
        "message": "I am very interested in this position and believe I would be a great fit."
    }
    resp = requests.post(f"{BASE_URL}/applications/", json=application_data)
    print_result("Create Job Application", resp)
    
    if resp.status_code == 200:
        application_id = resp.json().get("id")
        test_data['application_ids'].append(application_id)
        print(f"✅ Created application with ID: {application_id}")
    else:
        print("❌ Failed to create job application")
        return False
    
    # READ - Get all applications
    resp = requests.get(f"{BASE_URL}/applications/")
    print_result("Get All Applications", resp)
    
    # READ - Get applications for specific job
    resp = requests.get(f"{BASE_URL}/applications/job/{job_id}")
    print_result("Get Applications for Job", resp)
    
    # READ - Get specific application
    resp = requests.get(f"{BASE_URL}/applications/{application_id}")
    print_result("Get Specific Application", resp)
    
    # UPDATE - Update application status
    update_data = {
        "status": "accepted",
        "message": "Congratulations! Your application has been accepted."
    }
    resp = requests.put(f"{BASE_URL}/applications/{application_id}", json=update_data)
    print_result("Update Application Status", resp, 200)
    
    # DELETE - Delete application
    resp = requests.delete(f"{BASE_URL}/applications/{application_id}")
    print_result("Delete Application", resp, 200)
    
    if resp.status_code == 200:
        test_data['application_ids'].remove(application_id)
        print(f"✅ Deleted application with ID: {application_id}")
    
    return True

def cleanup_test_data():
    """Clean up all test data"""
    print("\n🧹 CLEANING UP TEST DATA")
    
    # Delete applications
    for app_id in test_data['application_ids']:
        resp = requests.delete(f"{BASE_URL}/applications/{app_id}")
        print(f"Deleted application {app_id}: {resp.status_code}")
    
    # Delete jobs
    for job_id in test_data['job_ids']:
        resp = requests.delete(f"{BASE_URL}/jobs/{job_id}")
        print(f"Deleted job {job_id}: {resp.status_code}")
    
    # Delete workers
    for worker_id in test_data['worker_ids']:
        resp = requests.delete(f"{BASE_URL}/workers/{worker_id}")
        print(f"Deleted worker {worker_id}: {resp.status_code}")
    
    # Delete business owners
    for bo_id in test_data['business_owner_ids']:
        resp = requests.delete(f"{BASE_URL}/business-owners/{bo_id}")
        print(f"Deleted business owner {bo_id}: {resp.status_code}")
    
    # Note: Users might not have delete endpoints, so we'll leave them
    print("✅ Cleanup completed")

def main():
    """Main test function"""
    print("🚀 WORKBEE API COMPREHENSIVE TEST SUITE")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Test JWT Authentication
        test_jwt_authentication()
        
        # Test User Operations
        if test_user_operations():
            # Test Business Owner Operations
            test_business_owner_operations()
            
            # Test Worker Operations
            test_worker_operations()
            
            # Test Job Operations
            test_job_operations()
            
            # Test Job Application Operations
            test_job_application_operations()
        
        # Cleanup
        cleanup_test_data()
        
        print("\n🎉 ALL TESTS COMPLETED!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        cleanup_test_data()

if __name__ == "__main__":
    main() 