import requests
import json
import os
import random
import string
import time

BASE_URL = "http://<your-vm-domain-or-ip>:8000"  # <-- Set your VM's public IP or domain here

# Test result tracking
test_results = {
    'total': 0,
    'expected': 0,
    'unexpected': 0,
    'details': []
}

# Helper to print test results and track them
def print_result(name, resp, expected_status=200, extra_check=None):
    test_results['total'] += 1
    
    # Determine if this is expected behavior
    is_expected = resp.status_code == expected_status
    if is_expected:
        test_results['expected'] += 1
    else:
        test_results['unexpected'] += 1
    
    # Store test details
    test_results['details'].append({
        'name': name,
        'status': resp.status_code,
        'expected': expected_status,
        'is_expected': is_expected
    })
    
    print(f"\n{'='*50}")
    print(f"🧪 {name}")
    print(f"{'='*50}")
    print(f"Status: {resp.status_code} {'✅' if is_expected else '❌'}")
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
    if extra_check:
        extra_check(resp)

# Helper to generate random strings
def rand_str(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to display dynamic summary
def display_summary():
    print("\n" + "="*60)
    print("📊 DYNAMIC TEST SUMMARY")
    print("="*60)
    print(f"Total test cases: {test_results['total']}")
    print(f"Expected behavior (✅): {test_results['expected']}")
    print(f"Unexpected behavior (❌): {test_results['unexpected']}")
    
    if test_results['unexpected'] > 0:
        print(f"\n❌ UNEXPECTED TEST RESULTS:")
        for test in test_results['details']:
            if not test['is_expected']:
                print(f"  - {test['name']}: Got {test['status']}, Expected {test['expected']}")
    
    success_rate = (test_results['expected'] / test_results['total'] * 100) if test_results['total'] > 0 else 0
    print(f"\nSuccess Rate: {success_rate:.1f}%")
    
    if test_results['unexpected'] == 0:
        print("🎉 All tests are passing as expected!")
    else:
        print(f"⚠️  {test_results['unexpected']} test(s) need attention.")
    print("="*60)

# Store created IDs for cleanup
test_data = {
    'user_ids': [],
    'business_owner_ids': [],
    'worker_ids': [],
    'job_ids': [],
    'application_ids': [],
    'tokens': {},
    'emails': set(),
}

def test_user_crud():
    print("\n=== USER CRUD & EDGE CASES ===")
    # Create user (valid)
    user_email = f"user_{rand_str()}@test.com"
    test_data['emails'].add(user_email)
    user_data = {
        "username": f"user_{rand_str()}",
        "email": user_email,
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    print_result("Create User (valid)", resp, 200)
    user_id = None
    if resp.status_code == 200:
        user_id = resp.json().get("id")
        test_data['user_ids'].append(user_id)
    # Create user (duplicate email)
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    print_result("Create User (duplicate email)", resp, 400)
    # Create user (missing fields)
    resp = requests.post(f"{BASE_URL}/users/register", json={"username": "abc"})
    print_result("Create User (missing fields)", resp, 422)
    # Login (valid)
    login_data = {"email": user_email, "password": "TestPass123!"}
    resp = requests.post(f"{BASE_URL}/users/login", json=login_data)
    print_result("User Login (valid)", resp, 200)
    token = None
    if resp.status_code == 200:
        token = resp.json().get("access_token")
        test_data['tokens']['user'] = token
    # Login (wrong password)
    resp = requests.post(f"{BASE_URL}/users/login", json={"email": user_email, "password": "wrongpass"})
    print_result("User Login (wrong password)", resp, 400)
    # Get me (unauthorized)
    resp = requests.get(f"{BASE_URL}/users/me")
    print_result("Get Me (unauthorized)", resp, 401)
    # Get me (authorized)
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_result("Get Me (authorized)", resp, 200)
    # Delete user (should fail, has no profile yet)
    if user_id:
        resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        print_result("Delete User (should succeed, no profile)", resp, 200)
        test_data['user_ids'].remove(user_id)

def test_business_owner_crud():
    print("\n=== BUSINESS OWNER CRUD & EDGE CASES ===")
    # Create a user for business owner
    user_email = f"bo_{rand_str()}@test.com"
    test_data['emails'].add(user_email)
    user_data = {
        "username": f"bo_{rand_str()}",
        "email": user_email,
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    user_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['user_ids'].append(user_id)
    # Create business owner (valid)
    bo_data = {
        "user_id": user_id,
        "business_name": f"Biz_{rand_str()}",
        "contact_person": "Owner Name",
        "contact_phone": "1234567890",
        "contact_email": user_email,
        "address": "123 Main St",
        "website": "https://biz.com",
        "industry": "Tech",
        "state": "CA",
        "city": "SF",
        "pincode": "94105",
        "year_established": 2020
    }
    resp = requests.post(f"{BASE_URL}/business-owners/", json=bo_data)
    print_result("Create Business Owner (valid)", resp, 200)
    bo_id = resp.json().get("id") if resp.status_code == 200 else None
    if bo_id:
        test_data['business_owner_ids'].append(bo_id)
    # Create business owner (non-existent user)
    bo_data_bad = bo_data.copy()
    bo_data_bad['user_id'] = 999999
    resp = requests.post(f"{BASE_URL}/business-owners/", json=bo_data_bad)
    print_result("Create Business Owner (non-existent user)", resp, 400)
    # Get all business owners
    resp = requests.get(f"{BASE_URL}/business-owners/")
    print_result("Get All Business Owners", resp, 200)
    # Get specific business owner
    if bo_id:
        resp = requests.get(f"{BASE_URL}/business-owners/{bo_id}")
        print_result("Get Business Owner (by id)", resp, 200)
    # Update business owner (valid)
    if bo_id:
        update_data = {"business_name": "Updated Biz", "contact_person": "New Owner"}
        resp = requests.put(f"{BASE_URL}/business-owners/{bo_id}", json=update_data)
        print_result("Update Business Owner (valid)", resp, 200)
    # Update business owner (invalid field)
    if bo_id:
        update_data = {"nonexistent_field": "value"}
        resp = requests.put(f"{BASE_URL}/business-owners/{bo_id}", json=update_data)
        print_result("Update Business Owner (invalid field)", resp, 200)
    # Delete business owner
    if bo_id:
        resp = requests.delete(f"{BASE_URL}/business-owners/{bo_id}")
        print_result("Delete Business Owner (valid)", resp, 200)
        test_data['business_owner_ids'].remove(bo_id)
    # Delete user (should succeed now)
    if user_id:
        resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        print_result("Delete User (after BO deleted)", resp, 200)
        test_data['user_ids'].remove(user_id)

def test_worker_crud():
    print("\n=== WORKER CRUD & EDGE CASES ===")
    # Create a user for worker
    user_email = f"worker_{rand_str()}@test.com"
    test_data['emails'].add(user_email)
    user_data = {
        "username": f"worker_{rand_str()}",
        "email": user_email,
        "password": "TestPass123!",
        "role": "seeker"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    user_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['user_ids'].append(user_id)
    # Create worker (valid)
    worker_data = {
        "user_id": user_id,
        "name": "Worker Name",
        "phone": "9876543210",
        "email": user_email,
        "skills": "Python,FastAPI",
        "years_of_experience": 2,
        "address": "456 Main St",
        "state": "CA",
        "city": "SF",
        "pincode": "94105"
    }
    resp = requests.post(f"{BASE_URL}/workers/", json=worker_data)
    print_result("Create Worker (valid)", resp, 200)
    worker_id = resp.json().get("id") if resp.status_code == 200 else None
    if worker_id:
        test_data['worker_ids'].append(worker_id)
    # Create worker (non-existent user)
    worker_data_bad = worker_data.copy()
    worker_data_bad['user_id'] = 999999
    resp = requests.post(f"{BASE_URL}/workers/", json=worker_data_bad)
    print_result("Create Worker (non-existent user)", resp, 400)
    # Get all workers
    resp = requests.get(f"{BASE_URL}/workers/")
    print_result("Get All Workers", resp, 200)
    # Get specific worker
    if worker_id:
        resp = requests.get(f"{BASE_URL}/workers/{worker_id}")
        print_result("Get Worker (by id)", resp, 200)
    # Update worker (valid)
    if worker_id:
        update_data = {"name": "Updated Worker", "skills": "Python,FastAPI,SQLAlchemy"}
        resp = requests.put(f"{BASE_URL}/workers/{worker_id}", json=update_data)
        print_result("Update Worker (valid)", resp, 200)
    # Update worker (invalid field)
    if worker_id:
        update_data = {"nonexistent_field": "value"}
        resp = requests.put(f"{BASE_URL}/workers/{worker_id}", json=update_data)
        print_result("Update Worker (invalid field)", resp, 200)
    # Delete worker
    if worker_id:
        resp = requests.delete(f"{BASE_URL}/workers/{worker_id}")
        print_result("Delete Worker (valid)", resp, 200)
        test_data['worker_ids'].remove(worker_id)
    # Delete user (should succeed now)
    if user_id:
        resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        print_result("Delete User (after Worker deleted)", resp, 200)
        test_data['user_ids'].remove(user_id)

def test_job_crud():
    print("\n=== JOB CRUD & EDGE CASES ===")
    # Create a business owner for job
    user_email = f"jobbo_{rand_str()}@test.com"
    test_data['emails'].add(user_email)
    user_data = {
        "username": f"jobbo_{rand_str()}",
        "email": user_email,
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    user_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['user_ids'].append(user_id)
    bo_data = {
        "user_id": user_id,
        "business_name": f"JobBiz_{rand_str()}",
        "contact_person": "Job Owner",
        "contact_phone": "1234567890",
        "contact_email": user_email,
        "address": "789 Main St",
        "website": "https://jobbiz.com",
        "industry": "Tech",
        "state": "CA",
        "city": "SF",
        "pincode": "94105",
        "year_established": 2020
    }
    resp = requests.post(f"{BASE_URL}/business-owners/", json=bo_data)
    bo_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['business_owner_ids'].append(bo_id)
    # Create job (valid)
    job_data = {
        "business_owner_id": bo_id,
        "title": "Test Job",
        "description": "A test job.",
        "required_skills": "Python,FastAPI",
        "location": "SF",
        "address": "789 Main St",
        "state": "CA",
        "city": "SF",
        "pincode": "94105",
        "hourly_rate": 50.0,
        "estimated_hours": 10,
        "start_date": "2024-08-15T09:00:00",
        "contact_person": "Job Owner",
        "contact_phone": "1234567890",
        "contact_email": user_email
    }
    resp = requests.post(f"{BASE_URL}/jobs/", json=job_data)
    print_result("Create Job (valid)", resp, 200)
    job_id = resp.json().get("id") if resp.status_code == 200 else None
    if job_id:
        test_data['job_ids'].append(job_id)
    # Create job (non-existent business owner)
    job_data_bad = job_data.copy()
    job_data_bad['business_owner_id'] = 999999
    resp = requests.post(f"{BASE_URL}/jobs/", json=job_data_bad)
    print_result("Create Job (non-existent business owner)", resp, 400)
    # Get all jobs
    resp = requests.get(f"{BASE_URL}/jobs/")
    print_result("Get All Jobs", resp, 200)
    # Get specific job
    if job_id:
        resp = requests.get(f"{BASE_URL}/jobs/{job_id}")
        print_result("Get Job (by id)", resp, 200)
    # Update job (valid)
    if job_id:
        update_data = {"title": "Updated Job", "hourly_rate": 60.0}
        resp = requests.put(f"{BASE_URL}/jobs/{job_id}", json=update_data)
        print_result("Update Job (valid)", resp, 200)
    # Update job (invalid field)
    if job_id:
        update_data = {"nonexistent_field": "value"}
        resp = requests.put(f"{BASE_URL}/jobs/{job_id}", json=update_data)
        print_result("Update Job (invalid field)", resp, 200)
    # Delete job
    if job_id:
        resp = requests.delete(f"{BASE_URL}/jobs/{job_id}")
        print_result("Delete Job (valid)", resp, 200)
        test_data['job_ids'].remove(job_id)
    # Delete business owner
    if bo_id:
        resp = requests.delete(f"{BASE_URL}/business-owners/{bo_id}")
        print_result("Delete Business Owner (after job deleted)", resp, 200)
        test_data['business_owner_ids'].remove(bo_id)
    # Delete user
    if user_id:
        resp = requests.delete(f"{BASE_URL}/users/{user_id}")
        print_result("Delete User (after BO deleted)", resp, 200)
        test_data['user_ids'].remove(user_id)

def test_application_crud():
    print("\n=== JOB APPLICATION CRUD & EDGE CASES ===")
    # Create a worker and job for application
    # Worker
    worker_email = f"appworker_{rand_str()}@test.com"
    test_data['emails'].add(worker_email)
    user_data = {
        "username": f"appworker_{rand_str()}",
        "email": worker_email,
        "password": "TestPass123!",
        "role": "seeker"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    worker_user_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['user_ids'].append(worker_user_id)
    worker_data = {
        "user_id": worker_user_id,
        "name": "App Worker",
        "phone": "5555555555",
        "email": worker_email,
        "skills": "Python,FastAPI",
        "years_of_experience": 1,
        "address": "App St",
        "state": "CA",
        "city": "SF",
        "pincode": "94105"
    }
    resp = requests.post(f"{BASE_URL}/workers/", json=worker_data)
    worker_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['worker_ids'].append(worker_id)
    # Business owner and job
    bo_email = f"appbo_{rand_str()}@test.com"
    test_data['emails'].add(bo_email)
    bo_user_data = {
        "username": f"appbo_{rand_str()}",
        "email": bo_email,
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=bo_user_data)
    bo_user_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['user_ids'].append(bo_user_id)
    bo_data = {
        "user_id": bo_user_id,
        "business_name": f"AppBO_{rand_str()}",
        "contact_person": "App BO",
        "contact_phone": "1111111111",
        "contact_email": bo_email,
        "address": "BO St",
        "website": "https://appbo.com",
        "industry": "Tech",
        "state": "CA",
        "city": "SF",
        "pincode": "94105",
        "year_established": 2020
    }
    resp = requests.post(f"{BASE_URL}/business-owners/", json=bo_data)
    bo_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['business_owner_ids'].append(bo_id)
    job_data = {
        "business_owner_id": bo_id,
        "title": "App Job",
        "description": "A job for app test.",
        "required_skills": "Python,FastAPI",
        "location": "SF",
        "address": "BO St",
        "state": "CA",
        "city": "SF",
        "pincode": "94105",
        "hourly_rate": 40.0,
        "estimated_hours": 5,
        "start_date": "2024-08-15T09:00:00",
        "contact_person": "App BO",
        "contact_phone": "1111111111",
        "contact_email": bo_email
    }
    resp = requests.post(f"{BASE_URL}/jobs/", json=job_data)
    job_id = resp.json().get("id") if resp.status_code == 200 else None
    test_data['job_ids'].append(job_id)
    # Create application (valid)
    app_data = {
        "job_id": job_id,
        "worker_id": worker_id,
        "message": "I want this job!"
    }
    resp = requests.post(f"{BASE_URL}/applications/", json=app_data)
    print_result("Create Application (valid)", resp, 200)
    app_id = resp.json().get("id") if resp.status_code == 200 else None
    if app_id:
        test_data['application_ids'].append(app_id)
    # Create application (non-existent job)
    app_data_bad = app_data.copy()
    app_data_bad['job_id'] = 999999
    resp = requests.post(f"{BASE_URL}/applications/", json=app_data_bad)
    print_result("Create Application (non-existent job)", resp, 400)
    # Create application (non-existent worker)
    app_data_bad = app_data.copy()
    app_data_bad['worker_id'] = 999999
    resp = requests.post(f"{BASE_URL}/applications/", json=app_data_bad)
    print_result("Create Application (non-existent worker)", resp, 400)
    # Get all applications
    resp = requests.get(f"{BASE_URL}/applications/")
    print_result("Get All Applications", resp, 200)
    # Get application by id
    if app_id:
        resp = requests.get(f"{BASE_URL}/applications/{app_id}")
        print_result("Get Application (by id)", resp, 200)
    # Update application (valid)
    if app_id:
        update_data = {"status": "accepted", "message": "Congrats!"}
        resp = requests.put(f"{BASE_URL}/applications/{app_id}", json=update_data)
        print_result("Update Application (valid)", resp, 200)
    # Update application (invalid field)
    if app_id:
        update_data = {"nonexistent_field": "value"}
        resp = requests.put(f"{BASE_URL}/applications/{app_id}", json=update_data)
        print_result("Update Application (invalid field)", resp, 200)
    # Delete application
    if app_id:
        resp = requests.delete(f"{BASE_URL}/applications/{app_id}")
        print_result("Delete Application (valid)", resp, 200)
        test_data['application_ids'].remove(app_id)
    # Delete job
    if job_id:
        resp = requests.delete(f"{BASE_URL}/jobs/{job_id}")
        print_result("Delete Job (after app deleted)", resp, 200)
        test_data['job_ids'].remove(job_id)
    # Delete business owner
    if bo_id:
        resp = requests.delete(f"{BASE_URL}/business-owners/{bo_id}")
        print_result("Delete Business Owner (after job deleted)", resp, 200)
        test_data['business_owner_ids'].remove(bo_id)
    # Delete worker
    if worker_id:
        resp = requests.delete(f"{BASE_URL}/workers/{worker_id}")
        print_result("Delete Worker (after app deleted)", resp, 200)
        test_data['worker_ids'].remove(worker_id)
    # Delete users
    for uid in [worker_user_id, bo_user_id]:
        if uid:
            resp = requests.delete(f"{BASE_URL}/users/{uid}")
            print_result(f"Delete User (after app deleted, id={uid})", resp, 200)
            test_data['user_ids'].remove(uid)

def test_additional_edge_cases():
    print("\n=== ADDITIONAL CORNER CASES & EDGE CASES ===")
    
    # Test extremely long inputs
    long_string = "a" * 1000
    user_data_long = {
        "username": long_string,
        "email": f"long_{rand_str()}@test.com",
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data_long)
    print_result("Create User (extremely long username)", resp, 422)
    
    # Test SQL injection attempts
    sql_injection_data = {
        "username": "user'; DROP TABLE users; --",
        "email": f"sql_{rand_str()}@test.com",
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=sql_injection_data)
    print_result("Create User (SQL injection attempt)", resp, 422)  # Should be blocked for security
    
    # Test XSS attempts
    xss_data = {
        "username": "<script>alert('xss')</script>",
        "email": f"xss_{rand_str()}@test.com",
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=xss_data)
    print_result("Create User (XSS attempt)", resp, 422)  # Should be blocked for security
    
    # Test invalid email formats
    invalid_emails = [
        "notanemail",
        "@nodomain.com",
        "nodomain@",
        "spaces in@email.com",
        "multiple@@at.com"
    ]
    for i, email in enumerate(invalid_emails):
        user_data = {
            "username": f"invalid_email_{i}",
            "email": email,
            "password": "TestPass123!",
            "role": "poster"
        }
        resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
        print_result(f"Create User (invalid email: {email})", resp, 422)
    
    # Test invalid phone numbers
    invalid_phones = ["abc", "123", "123-456", "123-456-789", "123-456-7890-1234-5678"]
    for phone in invalid_phones:
        # Create a user first
        user_email = f"phone_{rand_str()}@test.com"
        user_data = {
            "username": f"phone_{rand_str()}",
            "email": user_email,
            "password": "TestPass123!",
            "role": "poster"
        }
        resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
        user_id = resp.json().get("id") if resp.status_code == 200 else None
        if user_id:
            test_data['user_ids'].append(user_id)
            bo_data = {
                "user_id": user_id,
                "business_name": f"PhoneBiz_{rand_str()}",
                "contact_person": "Phone Owner",
                "contact_phone": phone,
                "contact_email": user_email,
                "address": "Phone St",
                "website": "https://phonebiz.com",
                "industry": "Tech",
                "state": "CA",
                "city": "SF",
                "pincode": "94105",
                "year_established": 2020
            }
            resp = requests.post(f"{BASE_URL}/business-owners/", json=bo_data)
            print_result(f"Create Business Owner (invalid phone: {phone})", resp, 422)
    
    # Test negative values
    user_email = f"negative_{rand_str()}@test.com"
    user_data = {
        "username": f"negative_{rand_str()}",
        "email": user_email,
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
    user_id = resp.json().get("id") if resp.status_code == 200 else None
    if user_id:
        test_data['user_ids'].append(user_id)
        bo_data = {
            "user_id": user_id,
            "business_name": f"NegativeBiz_{rand_str()}",
            "contact_person": "Negative Owner",
            "contact_phone": "1234567890",
            "contact_email": user_email,
            "address": "Negative St",
            "website": "https://negativebiz.com",
            "industry": "Tech",
            "state": "CA",
            "city": "SF",
            "pincode": "94105",
            "year_established": -2020  # Negative year
        }
        resp = requests.post(f"{BASE_URL}/business-owners/", json=bo_data)
        print_result("Create Business Owner (negative year)", resp, 422)
    
    # Test concurrent operations (simulate race conditions)
    concurrent_emails = [f"concurrent_{i}_{rand_str()}@test.com" for i in range(3)]
    for email in concurrent_emails:
        user_data = {
            "username": f"concurrent_{rand_str()}",
            "email": email,
            "password": "TestPass123!",
            "role": "poster"
        }
        resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
        print_result(f"Create User (concurrent: {email})", resp, 200)
        if resp.status_code == 200:
            test_data['user_ids'].append(resp.json().get("id"))
    
    # Test invalid HTTP methods
    resp = requests.patch(f"{BASE_URL}/users/1")
    print_result("PATCH on users (invalid method)", resp, 405)
    
    resp = requests.put(f"{BASE_URL}/users/")
    print_result("PUT on users collection (invalid method)", resp, 405)
    
    # Test non-existent resources
    resp = requests.get(f"{BASE_URL}/users/999999")
    print_result("Get non-existent user", resp, 404)
    
    resp = requests.put(f"{BASE_URL}/users/999999", json={"username": "test"})
    print_result("Update non-existent user", resp, 404)
    
    resp = requests.delete(f"{BASE_URL}/users/999999")
    print_result("Delete non-existent user", resp, 404)
    
    # Test malformed JSON
    headers = {"Content-Type": "application/json"}
    resp = requests.post(f"{BASE_URL}/users/register", data="invalid json", headers=headers)
    print_result("Create User (malformed JSON)", resp, 422)
    
    # Test empty request body
    resp = requests.post(f"{BASE_URL}/users/register", json={})
    print_result("Create User (empty body)", resp, 422)
    
    # Test JWT token edge cases
    # Invalid token
    headers = {"Authorization": "Bearer invalid_token"}
    resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_result("Get Me (invalid JWT)", resp, 401)
    
    # Expired token (if you have a way to generate one)
    # Malformed token
    headers = {"Authorization": "Bearer not.a.valid.token"}
    resp = requests.get(f"{BASE_URL}/users/me", headers=headers)
    print_result("Get Me (malformed JWT)", resp, 401)
    
    # Test rate limiting (if implemented)
    for i in range(10):
        resp = requests.post(f"{BASE_URL}/users/register", json={
            "username": f"rate_limit_{i}_{rand_str()}",
            "email": f"rate_limit_{i}_{rand_str()}@test.com",
            "password": "TestPass123!",
            "role": "poster"
        })
        if resp.status_code != 200:
            print_result(f"Rate limiting test {i}", resp, 429)
            break
    
    # Test very large payloads
    large_payload = {
        "username": "large_user",
        "email": f"large_{rand_str()}@test.com",
        "password": "TestPass123!" * 1000,  # Very large password
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=large_payload)
    print_result("Create User (very large payload)", resp, 422)
    
    # Test special characters in inputs
    special_chars_data = {
        "username": "user!@#$%^&*()_+-=[]{}|;':\",./<>?",
        "email": f"special_{rand_str()}@test.com",
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=special_chars_data)
    print_result("Create User (special characters in username)", resp, 422)  # Should be blocked for security
    if resp.status_code == 200:
        test_data['user_ids'].append(resp.json().get("id"))
    
    # Test Unicode characters
    unicode_data = {
        "username": "user_🚀_🌟_🎉",
        "email": f"unicode_{rand_str()}@test.com",
        "password": "TestPass123!",
        "role": "poster"
    }
    resp = requests.post(f"{BASE_URL}/users/register", json=unicode_data)
    print_result("Create User (Unicode characters)", resp, 422)  # Should be blocked for security
    if resp.status_code == 200:
        test_data['user_ids'].append(resp.json().get("id"))

def test_performance_edge_cases():
    print("\n=== PERFORMANCE & STRESS EDGE CASES ===")
    
    # Test creating many users quickly
    print("Creating 5 users quickly...")
    for i in range(5):
        user_data = {
            "username": f"perf_{i}_{rand_str()}",
            "email": f"perf_{i}_{rand_str()}@test.com",
            "password": "TestPass123!",
            "role": "poster"
        }
        resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
        if resp.status_code == 200:
            test_data['user_ids'].append(resp.json().get("id"))
    
    # Test getting all users (should handle large datasets)
    resp = requests.get(f"{BASE_URL}/users/")
    print_result("Get all users (performance test)", resp, 200)
    
    # Test getting all business owners
    resp = requests.get(f"{BASE_URL}/business-owners/")
    print_result("Get all business owners (performance test)", resp, 200)
    
    # Test getting all workers
    resp = requests.get(f"{BASE_URL}/workers/")
    print_result("Get all workers (performance test)", resp, 200)
    
    # Test getting all jobs
    resp = requests.get(f"{BASE_URL}/jobs/")
    print_result("Get all jobs (performance test)", resp, 200)
    
    # Test getting all applications
    resp = requests.get(f"{BASE_URL}/applications/")
    print_result("Get all applications (performance test)", resp, 200)

def main():
    print("\n========== WORKBEE VM API EXTREME EDGE CASE TEST SUITE ==========")
    test_user_crud()
    test_business_owner_crud()
    test_worker_crud()
    test_job_crud()
    test_application_crud()
    test_additional_edge_cases()
    test_performance_edge_cases()
    display_summary()
    print("\nAll tests completed. Check above for any ❌ failures.")

if __name__ == "__main__":
    main() 