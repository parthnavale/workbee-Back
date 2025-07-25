import requests
import json
import time

BASE_URL = "https://myworkbee.duckdns.org"

# Utility to print request/response details
def print_response(resp, label=None):
    if label:
        print(f"\n=== {label} ===")
    print(f"URL: {resp.request.url}")
    print(f"Method: {resp.request.method}")
    print(f"Request Body: {resp.request.body}")
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
    print("-" * 60)

def main():
    # Store created object IDs for cleanup
    created = {}
    session = requests.Session()
    unique = str(int(time.time()))
    
    # Track test results
    test_results = []
    def record_result(label, resp, expect_status=None):
        passed = (expect_status is None and resp.ok) or (expect_status is not None and resp.status_code == expect_status)
        test_results.append({
            "label": label,
            "status_code": resp.status_code,
            "passed": passed,
            "response": resp.text
        })
        print_response(resp, label)

    # 1. Register a user (worker)
    user_worker = {
        "username": f"testworker_{unique}",
        "email": f"testworker_{unique}@example.com",
        "password": "123456",
        "role": "seeker"
    }
    resp = session.post(f"{BASE_URL}/users/register", json=user_worker)
    record_result("Register Worker User", resp, 200)
    created["user_worker_id"] = resp.json().get("id") if resp.ok else None

    # 2. Register a user (business owner)
    user_owner = {
        "username": f"testowner_{unique}",
        "email": f"testowner_{unique}@example.com",
        "password": "123456",
        "role": "poster"
    }
    resp = session.post(f"{BASE_URL}/users/register", json=user_owner)
    record_result("Register Owner User", resp, 200)
    created["user_owner_id"] = resp.json().get("id") if resp.ok else None

    # 3. Test duplicate registration (should fail)
    resp = session.post(f"{BASE_URL}/users/register", json=user_worker)
    record_result("Duplicate Worker Registration (Expect 400)", resp, 400)

    # 4. Login as worker
    login_worker = {"email": user_worker["email"], "password": "123456"}
    resp = session.post(f"{BASE_URL}/users/login", json=login_worker)
    record_result("Login Worker", resp, 200)
    worker_token = resp.json().get("access_token") if resp.ok else None
    created["worker_token"] = worker_token
    created["worker_email"] = user_worker["email"]

    # 5. Login as owner
    login_owner = {"email": user_owner["email"], "password": "123456"}
    resp = session.post(f"{BASE_URL}/users/login", json=login_owner)
    record_result("Login Owner", resp, 200)
    owner_token = resp.json().get("access_token") if resp.ok else None
    created["owner_token"] = owner_token
    created["owner_email"] = user_owner["email"]

    # 6. Create worker profile
    worker_profile = {
        "user_id": created["user_worker_id"],
        "name": "Test Worker",
        "phone": "1234567890",
        "email": user_worker["email"],
        "skills": "Testing,API",
        "years_of_experience": 2,
        "address": "123 Test Lane",
        "state": "TestState",
        "city": "TestCity",
        "pincode": "123456",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "fcm_token": f"dummy_token_{unique}"
    }
    resp = session.post(f"{BASE_URL}/workers/", json=worker_profile)
    record_result("Create Worker Profile", resp, 200)
    created["worker_id"] = resp.json().get("id") if resp.ok else None

    # 7. Create business owner profile
    owner_profile = {
        "user_id": created["user_owner_id"],
        "name": "Test Owner",
        "phone": "9876543210",
        "email": user_owner["email"],
        "business_name": "Test Business",
        "address": "456 Owner Lane",
        "state": "OwnerState",
        "city": "OwnerCity",
        "pincode": "654321",
        "fcm_token": f"dummy_token_{unique}"
    }
    resp = session.post(f"{BASE_URL}/business-owners/", json=owner_profile)
    record_result("Create Business Owner Profile", resp, 200)
    created["owner_id"] = resp.json().get("id") if resp.ok else None

    # 8. Create a job (as owner)
    job = {
        "title": "API Test Job",
        "description": "A job for API testing.",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "business_owner_id": created["owner_id"]
    }
    resp = session.post(f"{BASE_URL}/jobs/", json=job)
    record_result("Create Job", resp, 200)
    created["job_id"] = resp.json().get("id") if resp.ok else None

    # 9. Get all jobs
    resp = session.get(f"{BASE_URL}/jobs/")
    record_result("Get All Jobs", resp, 200)

    # 10. Get nearby jobs
    params = {"lat": 19.0760, "lng": 72.8777, "radius_km": 10}
    resp = session.get(f"{BASE_URL}/jobs/nearby", params=params)
    record_result("Get Nearby Jobs", resp, 200)

    # 11. Apply for job (as worker)
    application = {
        "worker_id": created["worker_id"],
        "job_id": created["job_id"]
    }
    resp = session.post(f"{BASE_URL}/applications/", json=application)
    record_result("Apply for Job", resp, 200)
    created["application_id"] = resp.json().get("id") if resp.ok else None

    # 12. Duplicate application (should fail)
    resp = session.post(f"{BASE_URL}/applications/", json=application)
    record_result("Duplicate Application (Expect 400)", resp, 400)

    # 13. Get applications by worker
    resp = session.get(f"{BASE_URL}/applications/worker/{created['worker_id']}")
    record_result("Get Applications by Worker", resp, 200)

    # 14. Get notifications for worker
    resp = session.get(f"{BASE_URL}/notifications/{created['worker_id']}")
    record_result("Get Notifications for Worker", resp, 200)
    notif_ids = [n.get("id") for n in resp.json()] if resp.ok else []

    # 15. Mark notifications as read
    if notif_ids:
        resp = session.post(f"{BASE_URL}/notifications/mark_read", json={"notification_ids": notif_ids})
        record_result("Mark Notifications as Read", resp, 200)

    # 16. Force FCM notification (should succeed)
    resp = session.post(f"{BASE_URL}/notifications/force_fcm/{created['worker_id']}?title=Test&body=This%20is%20a%20test%20notification")
    record_result("Force FCM Notification", resp, 200)

    # 17. Test error: get non-existent worker
    resp = session.get(f"{BASE_URL}/workers/999999")
    record_result("Get Non-existent Worker (Expect 404)", resp, 404)

    # 18. Test error: delete non-existent job
    resp = session.delete(f"{BASE_URL}/jobs/999999")
    record_result("Delete Non-existent Job (Expect 404)", resp, 404)

    # 19. Cleanup: delete application
    if created.get("application_id"):
        resp = session.delete(f"{BASE_URL}/applications/{created['application_id']}")
        record_result("Delete Application (Cleanup)", resp, 200)

    # --- NEW: Delete notifications for the worker before deleting job/worker/owner ---
    notif_ids = []
    resp = session.get(f"{BASE_URL}/notifications/{created['worker_id']}")
    if resp.ok:
        notif_ids = [n.get("id") for n in resp.json()]
        for notif_id in notif_ids:
            del_resp = session.delete(f"{BASE_URL}/notifications/id/{notif_id}")
            record_result(f"Delete Notification {notif_id} (Cleanup)", del_resp, 200)

    # 20. Cleanup: delete job
    if created.get("job_id"):
        resp = session.delete(f"{BASE_URL}/jobs/{created['job_id']}")
        record_result("Delete Job (Cleanup)", resp, 200)

    # 21. Cleanup: delete worker profile
    if created.get("worker_id"):
        resp = session.delete(f"{BASE_URL}/workers/{created['worker_id']}")
        record_result("Delete Worker (Cleanup)", resp, 200)

    # 22. Cleanup: delete business owner profile
    if created.get("owner_id"):
        resp = session.delete(f"{BASE_URL}/business-owners/{created['owner_id']}")
        record_result("Delete Business Owner (Cleanup)", resp, 200)

    # 23. Cleanup: delete users
    if created.get("user_worker_id"):
        resp = session.delete(f"{BASE_URL}/users/{created['user_worker_id']}")
        record_result("Delete Worker User (Cleanup)", resp, 200)
    if created.get("user_owner_id"):
        resp = session.delete(f"{BASE_URL}/users/{created['user_owner_id']}")
        record_result("Delete Owner User (Cleanup)", resp, 200)

    # --- Summary ---
    print("\n=== TEST SUMMARY ===")
    passed = sum(1 for r in test_results if r["passed"])
    failed = sum(1 for r in test_results if not r["passed"])
    print(f"Total tests: {len(test_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("\nDetailed Results:")
    for r in test_results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"{status}: {r['label']} (Status: {r['status_code']})")

if __name__ == "__main__":
    main() 