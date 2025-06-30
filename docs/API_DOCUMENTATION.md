# Workbee Backend API Documentation

This document describes the REST API endpoints, request/response schemas, and example payloads for the Workbee job marketplace backend.

---

## Authentication

### Register User
- **POST** `/users/register`
- **Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "yourpassword",
  "role": "seeker" // or "poster"
}
```
- **Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "role": "seeker"
}
```

### Login
- **POST** `/users/login`
- **Request Body:**
```json
{
  "email": "john@example.com",
  "password": "yourpassword"
}
```
- **Response:**
```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

## Business Owners

### Create Business Owner
- **POST** `/business-owners/`
- **Request Body:**
```json
{
  "user_id": 1,
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
```
- **Response:**
```json
{
  "id": 1,
  "user_id": 1,
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
```

### Get Business Owner by ID
- **GET** `/business-owners/{owner_id}`
- **Response:** _Same as above_

### Get All Business Owners
- **GET** `/business-owners/`
- **Response:**
```json
[
  { /* BusinessOwnerResponse */ }, ...
]
```

### Update Business Owner
- **PUT** `/business-owners/{owner_id}`
- **Request Body:** _Same as create_
- **Response:** _Same as above_

### Delete Business Owner
- **DELETE** `/business-owners/{owner_id}`
- **Response:**
```json
{"detail": "Business owner deleted"}
```

---

## Workers

### Create Worker
- **POST** `/workers/`
- **Request Body:**
```json
{
  "user_id": 2,
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
```
- **Response:**
```json
{
  "id": 1,
  "user_id": 2,
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
```

### Get Worker by ID
- **GET** `/workers/{worker_id}`
- **Response:** _Same as above_

### Get All Workers
- **GET** `/workers/`
- **Response:**
```json
[
  { /* WorkerResponse */ }, ...
]
```

### Update Worker
- **PUT** `/workers/{worker_id}`
- **Request Body:** _Same as create_
- **Response:** _Same as above_

### Delete Worker
- **DELETE** `/workers/{worker_id}`
- **Response:**
```json
{"detail": "Worker deleted"}
```

---

## Jobs

### Create Job
- **POST** `/jobs/`
- **Request Body:**
```json
{
  "business_owner_id": 1,
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
```
- **Response:**
```json
{
  "id": 1,
  "business_owner_id": 1,
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
  "contact_email": "alice@acme.com",
  "posted_date": "2024-06-30T12:00:00",
  "status": "open"
}
```

### Get Job by ID
- **GET** `/jobs/{job_id}`
- **Response:** _Same as above_

### Get All Jobs
- **GET** `/jobs/`
- **Response:**
```json
[
  { /* JobResponse */ }, ...
]
```

### Get Jobs by Business Owner
- **GET** `/jobs/business/{business_owner_id}`
- **Response:**
```json
[
  { /* JobResponse */ }, ...
]
```

### Update Job
- **PUT** `/jobs/{job_id}`
- **Request Body:** _Same as create_
- **Response:** _Same as above_

### Delete Job
- **DELETE** `/jobs/{job_id}`
- **Response:**
```json
{"detail": "Job deleted"}
```

---

## Job Applications

### Apply for Job
- **POST** `/applications/`
- **Request Body:**
```json
{
  "job_id": 1,
  "worker_id": 2,
  "message": "I am interested in this job."
}
```
- **Response:**
```json
{
  "id": 1,
  "job_id": 1,
  "worker_id": 2,
  "message": "I am interested in this job.",
  "status": "pending",
  "applied_date": "2024-06-30T12:00:00",
  "responded_date": null
}
```

### Get Application by ID
- **GET** `/applications/{application_id}`
- **Response:** _Same as above_

### Get All Applications
- **GET** `/applications/`
- **Response:**
```json
[
  { /* JobApplicationResponse */ }, ...
]
```

### Get Applications by Job
- **GET** `/applications/job/{job_id}`
- **Response:**
```json
[
  { /* JobApplicationResponse */ }, ...
]
```

### Get Applications by Worker
- **GET** `/applications/worker/{worker_id}`
- **Response:**
```json
[
  { /* JobApplicationResponse */ }, ...
]
```

### Update Application
- **PUT** `/applications/{application_id}`
- **Request Body:** _Same as create_
- **Response:** _Same as above_

### Delete Application
- **DELETE** `/applications/{application_id}`
- **Response:**
```json
{"detail": "Application deleted"}
```

---

## Database Configuration

The backend is now configured to use **MySQL** by default.

- The connection string is set in `workbee-Back/core/database.py`:
  ```python
  SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Parth%402000@localhost:3306/workbee_db"
  ```
- If your MySQL password contains special characters (like `@`), encode them (e.g., `@` becomes `%40`).
- Make sure the database `workbee_db` exists and your MySQL server is running.
- Install the MySQL connector:
  ```bash
  pip install mysql-connector-python
  ```

You can change the connection string to match your own MySQL credentials and host as needed.

---

## How to Run in Production

To run the Workbee backend in a production-grade environment, follow these steps:

### 1. Install Production Dependencies
Make sure you have `gunicorn` and `uvicorn` installed:
```bash
pip install gunicorn uvicorn
```

### 2. Set Environment Variables
Set environment variables for security and configuration (example for Linux):
```bash
export WORKBEE_SECRET_KEY="your-very-secret-key"
export WORKBEE_DATABASE_URL="sqlite:///./workbee.db"  # Or your production DB URL
```

### 3. Run with Gunicorn and Uvicorn Workers
Use Gunicorn with Uvicorn workers for robust, multi-process serving:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker workbee-Back.main:app --bind 0.0.0.0:8000
```
- `-w 4` sets 4 worker processes (adjust based on your CPU cores)
- `--bind 0.0.0.0:8000` makes the app accessible on all interfaces

### 4. Use a Process Manager (Optional but Recommended)
For automatic restarts and monitoring, use a process manager like `systemd`, `supervisor`, or `pm2`.

### 5. Reverse Proxy (Recommended)
Put a reverse proxy (like Nginx or Caddy) in front of Gunicorn for SSL, compression, and security.

### 6. Static Files & CORS
- Serve static files (if any) via your reverse proxy.
- Adjust CORS settings in `main.py` for your frontend domain.

### 7. Logs & Monitoring
- Monitor logs from Gunicorn and your process manager.
- Set up alerts for errors and downtime.

---

For more details, see the [FastAPI deployment docs](https://fastapi.tiangolo.com/deployment/). 