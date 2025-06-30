import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Helper to print test results
def print_result(name, resp):
    print(f"\n{name}")
    print(f"Status: {resp.status_code}")
    try:
        print(json.dumps(resp.json(), indent=2))
    except Exception:
        print(resp.text)

# 1. Register a user (business owner)
user_data = {
    "username": "owner1",
    "email": "owner1@example.com",
    "password": "password123",
    "role": "poster"
}
resp = requests.post(f"{BASE_URL}/users/register", json=user_data)
print_result("Register User (Business Owner)", resp)
user_id = resp.json().get("id")

# 2. Register a user (worker)
worker_user_data = {
    "username": "worker1",
    "email": "worker1@example.com",
    "password": "password123",
    "role": "seeker"
}
resp = requests.post(f"{BASE_URL}/users/register", json=worker_user_data)
print_result("Register User (Worker)", resp)
worker_user_id = resp.json().get("id")

# 3. Create a business owner (requires user_id)
business_owner_data = {
    "user_id": user_id,
    "business_name": "Acme Corp",
    "contact_person": "Alice",
    "contact_phone": "1234567890",
    "contact_email": "alice@acme.com",
    "address": "123 Main St",
    "website": "https://acme.com",
    "industry": "Retail",
    "state": "CA",
    "city": "San Francisco",
    "pincode": "94105",
    "year_established": 2010
}
resp = requests.post(f"{BASE_URL}/business-owners/", json=business_owner_data)
print_result("Create Business Owner", resp)
business_owner_id = resp.json().get("id")

# 4. Create a worker (requires user_id)
worker_data = {
    "user_id": worker_user_id,
    "name": "Bob",
    "phone": "9876543210",
    "email": "bob@example.com",
    "skills": "Cashier,Inventory",
    "years_of_experience": 3,
    "address": "456 Park Ave",
    "state": "CA",
    "city": "San Francisco",
    "pincode": "94107"
}
resp = requests.post(f"{BASE_URL}/workers/", json=worker_data)
print_result("Create Worker", resp)
worker_id = resp.json().get("id")

# 5. Create a job (requires business_owner_id)
job_data = {
    "business_owner_id": business_owner_id,
    "title": "Cashier Needed",
    "description": "Looking for a cashier...",
    "required_skills": "Cashier,POS",
    "location": "San Francisco",
    "address": "123 Main St",
    "state": "CA",
    "city": "San Francisco",
    "pincode": "94105",
    "hourly_rate": 20.5,
    "estimated_hours": 40,
    "start_date": "2024-07-01T09:00:00",
    "contact_person": "Alice",
    "contact_phone": "1234567890",
    "contact_email": "alice@acme.com"
}
resp = requests.post(f"{BASE_URL}/jobs/", json=job_data)
print_result("Create Job", resp)
job_id = resp.json().get("id")

# 6. Apply for a job (requires job_id and worker_id)
application_data = {
    "job_id": job_id,
    "worker_id": worker_id,
    "message": "I am interested in this job."
}
resp = requests.post(f"{BASE_URL}/applications/", json=application_data)
print_result("Apply for Job", resp)
application_id = resp.json().get("id")

# 7. Get all jobs
resp = requests.get(f"{BASE_URL}/jobs/")
print_result("Get All Jobs", resp)

# 8. Get all applications for the job
resp = requests.get(f"{BASE_URL}/applications/job/{job_id}")
print_result("Get Applications for Job", resp)

# 9. Get all workers
resp = requests.get(f"{BASE_URL}/workers/")
print_result("Get All Workers", resp)

# 10. Get all business owners
resp = requests.get(f"{BASE_URL}/business-owners/")
print_result("Get All Business Owners", resp) 