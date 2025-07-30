#!/usr/bin/env python3
"""
Test script for role-based access control
"""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"  # Change to your server URL

def test_role_access_control():
    """Test role-based access control"""
    
    print("🧪 Testing Role-Based Access Control")
    print("=" * 50)
    
    # Test data
    business_owner_data = {
        "username": "business_owner",
        "email": "business@test.com",
        "password": "password123",
        "role": "poster"
    }
    
    worker_data = {
        "username": "worker_user",
        "email": "worker@test.com",
        "password": "password123",
        "role": "seeker"
    }
    
    # Step 1: Register users
    print("\n📝 Step 1: Registering users")
    print("-" * 30)
    
    # Register business owner
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=business_owner_data)
        if response.status_code == 200:
            business_owner = response.json()
            print(f"✅ Registered business owner: {business_owner['username']}")
        else:
            print(f"❌ Failed to register business owner: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error registering business owner: {str(e)}")
        return
    
    # Register worker
    try:
        response = requests.post(f"{BASE_URL}/users/register", json=worker_data)
        if response.status_code == 200:
            worker = response.json()
            print(f"✅ Registered worker: {worker['username']}")
        else:
            print(f"❌ Failed to register worker: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error registering worker: {str(e)}")
        return
    
    # Step 2: Login and get tokens
    print("\n🔑 Step 2: Getting access tokens")
    print("-" * 30)
    
    # Login as business owner
    try:
        response = requests.post(f"{BASE_URL}/users/login", json={
            "email": business_owner_data["email"],
            "password": business_owner_data["password"]
        })
        if response.status_code == 200:
            business_owner_token = response.json()["access_token"]
            print(f"✅ Business owner token obtained")
        else:
            print(f"❌ Failed to login business owner: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error logging in business owner: {str(e)}")
        return
    
    # Login as worker
    try:
        response = requests.post(f"{BASE_URL}/users/login", json={
            "email": worker_data["email"],
            "password": worker_data["password"]
        })
        if response.status_code == 200:
            worker_token = response.json()["access_token"]
            print(f"✅ Worker token obtained")
        else:
            print(f"❌ Failed to login worker: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error logging in worker: {str(e)}")
        return
    
    # Step 3: Test access control
    print("\n🚫 Step 3: Testing access restrictions")
    print("-" * 30)
    
    headers_business = {"Authorization": f"Bearer {business_owner_token}"}
    headers_worker = {"Authorization": f"Bearer {worker_token}"}
    
    # Test 1: Business owner trying to access worker endpoints
    print("\n🔍 Test 1: Business owner accessing worker endpoints")
    
    # Try to get worker profile (should fail)
    try:
        response = requests.get(f"{BASE_URL}/workers/my-profile", headers=headers_business)
        if response.status_code == 403:
            print("✅ Business owner correctly blocked from worker endpoints")
        else:
            print(f"❌ Business owner should be blocked but got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing business owner access: {str(e)}")
    
    # Test 2: Worker trying to access business owner endpoints
    print("\n🔍 Test 2: Worker accessing business owner endpoints")
    
    # Try to get business owner profile (should fail)
    try:
        response = requests.get(f"{BASE_URL}/business-owners/my-profile", headers=headers_worker)
        if response.status_code == 403:
            print("✅ Worker correctly blocked from business owner endpoints")
        else:
            print(f"❌ Worker should be blocked but got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing worker access: {str(e)}")
    
    # Test 3: Business owner accessing their own endpoints
    print("\n🔍 Test 3: Business owner accessing their own endpoints")
    
    # Try to get business owner profile (should work)
    try:
        response = requests.get(f"{BASE_URL}/business-owners/my-profile", headers=headers_business)
        if response.status_code == 404:
            print("✅ Business owner can access endpoint (no profile yet)")
        elif response.status_code == 200:
            print("✅ Business owner can access their profile")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing business owner self-access: {str(e)}")
    
    # Test 4: Worker accessing their own endpoints
    print("\n🔍 Test 4: Worker accessing their own endpoints")
    
    # Try to get worker profile (should work)
    try:
        response = requests.get(f"{BASE_URL}/workers/my-profile", headers=headers_worker)
        if response.status_code == 404:
            print("✅ Worker can access endpoint (no profile yet)")
        elif response.status_code == 200:
            print("✅ Worker can access their profile")
        else:
            print(f"❌ Unexpected response: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing worker self-access: {str(e)}")
    
    # Test 5: Unauthenticated access
    print("\n🔍 Test 5: Unauthenticated access")
    
    # Try to access protected endpoints without token
    try:
        response = requests.get(f"{BASE_URL}/business-owners/my-profile")
        if response.status_code == 401:
            print("✅ Unauthenticated access correctly blocked")
        else:
            print(f"❌ Unauthenticated access should be blocked but got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing unauthenticated access: {str(e)}")
    
    # Test 6: Create profiles and test ownership
    print("\n🔍 Test 6: Testing profile ownership")
    
    # Create business owner profile
    business_profile_data = {
        "user_id": business_owner["id"],
        "business_name": "Test Business",
        "contact_person": "John Doe",
        "contact_phone": "9876543210",
        "contact_email": "contact@testbusiness.com"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/business-owners/", json=business_profile_data, headers=headers_business)
        if response.status_code == 200:
            business_profile = response.json()
            print(f"✅ Created business owner profile: {business_profile['business_name']}")
            
            # Try to access someone else's profile (should fail)
            fake_id = business_profile["id"] + 999
            response = requests.get(f"{BASE_URL}/business-owners/{fake_id}", headers=headers_business)
            if response.status_code == 404:
                print("✅ Correctly blocked access to non-existent profile")
            else:
                print(f"❌ Unexpected response for non-existent profile: {response.status_code}")
                
        else:
            print(f"❌ Failed to create business profile: {response.text}")
    except Exception as e:
        print(f"❌ Error creating business profile: {str(e)}")
    
    # Create worker profile
    worker_profile_data = {
        "user_id": worker["id"],
        "name": "Test Worker",
        "phone": "9876543210",
        "email": "worker@test.com",
        "skills": "Python, FastAPI",
        "years_of_experience": 2,
        "address": "Test Address",
        "state": "Maharashtra",
        "city": "Mumbai",
        "pincode": "400001"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/workers/", json=worker_profile_data, headers=headers_worker)
        if response.status_code == 200:
            worker_profile = response.json()
            print(f"✅ Created worker profile: {worker_profile['name']}")
            
            # Try to access someone else's profile (should fail)
            fake_id = worker_profile["id"] + 999
            response = requests.get(f"{BASE_URL}/workers/{fake_id}", headers=headers_worker)
            if response.status_code == 404:
                print("✅ Correctly blocked access to non-existent profile")
            else:
                print(f"❌ Unexpected response for non-existent profile: {response.status_code}")
                
        else:
            print(f"❌ Failed to create worker profile: {response.text}")
    except Exception as e:
        print(f"❌ Error creating worker profile: {str(e)}")
    
    # Test 7: Test admin-only endpoints
    print("\n🔍 Test 7: Testing admin-only endpoints")
    
    # Try to access admin endpoints with non-admin users
    try:
        response = requests.get(f"{BASE_URL}/business-owners/", headers=headers_business)
        if response.status_code == 403:
            print("✅ Non-admin users correctly blocked from admin endpoints")
        else:
            print(f"❌ Non-admin users should be blocked but got: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing admin endpoint access: {str(e)}")
    
    print("\n✅ Role-Based Access Control Tests Completed!")

if __name__ == "__main__":
    test_role_access_control() 