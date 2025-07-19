# Workbee Backend API Documentation

**Production URL**: https://myworkbee.duckdns.org  
**Interactive Docs**: https://myworkbee.duckdns.org/docs  
**WebSocket**: wss://myworkbee.duckdns.org/ws/notifications/{user_id}  
**Test Coverage**: 100% (80 test cases)  

This document describes the REST API endpoints, WebSocket connections, request/response schemas, validation rules, and example payloads for the Workbee job marketplace backend.

---

## 🚀 Production Status

✅ **Fully Deployed**: Running on GCP VM with HTTPS  
✅ **Domain**: https://myworkbee.duckdns.org  
✅ **WebSocket**: Real-time notifications via WSS  
✅ **SSL Certificate**: Let's Encrypt (auto-renewal)  
✅ **Database**: MySQL with foreign key constraints  
✅ **Test Coverage**: 100% success rate  

---

## 🔐 Authentication

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
- **Validation Rules:**
  - Username: Alphanumeric with underscores only
  - Email: Valid email format
  - Password: Minimum length and complexity
  - Role: Must be "seeker" or "poster"
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

### Get Current User (Protected)
- **GET** `/users/me`
- **Headers:** `Authorization: Bearer <JWT_TOKEN>`
- **Response:** Same as register response

---

## 🔌 Real-time Notifications (WebSocket)

### WebSocket Connection
- **URL**: `wss://myworkbee.duckdns.org/ws/notifications/{user_id}`
- **Protocol**: WebSocket Secure (WSS)
- **Authentication**: User ID in URL path

### Connection Example
```javascript
// Connect to WebSocket for real-time notifications
const userId = 123; // Worker or Business Owner ID
const ws = new WebSocket(`wss://myworkbee.duckdns.org/ws/notifications/${userId}`);

// Handle incoming messages
ws.onmessage = function(event) {
    const notification = JSON.parse(event.data);
    console.log('New notification:', notification);
    
    // Handle different notification types
    switch(notification.type) {
        case 'new_application':
            // New job application received
            break;
        case 'application_status':
            // Application status updated
            break;
        case 'job_update':
            // Job details updated
            break;
    }
};

// Handle connection events
ws.onopen = function() {
    console.log('WebSocket connected');
};

ws.onclose = function() {
    console.log('WebSocket disconnected');
};

ws.onerror = function(error) {
    console.error('WebSocket error:', error);
};
```

### Notification Types
- **New Application**: Sent to business owners when workers apply for jobs
- **Application Status**: Sent to workers when applications are accepted/rejected
- **Job Updates**: Real-time updates for job status changes

### Notification Format
```json
{
  "type": "new_application",
  "message": "New application received for 'Cashier Position'",
  "data": {
    "job_id": 123,
    "application_id": 456,
    "worker_name": "John Doe",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

---

## 👥 Users

### Get All Users
- **GET** `/users/`
- **Response:**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "role": "seeker"
  }
]
```

### Get User by ID
- **GET** `/users/{user_id}`
- **Response:** Same as register response

### Update User
- **PUT** `/users/{user_id}`
- **Request Body:** Same as register (all fields optional)
- **Response:** Same as register response

### Delete User
- **DELETE** `/users/{user_id}`
- **Note:** Can only delete users without associated profiles
- **Response:**
```json
{"detail": "User deleted"}
```

---

## 🏢 Business Owners

### Create Business Owner
- **POST** `/business-owners/`
- **Request Body:**
```json
{
  "user_id": 1,
  "business_name": "Acme Corp",
  "contact_person": "Alice",
  "contact_phone": "9876543210",
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
- **Validation Rules:**
  - Phone: 10-15 digits, Indian numbers start with 6,7,8,9
  - Year: Between 1800-2100
  - Email: Valid email format
  - User must exist in database
- **Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "business_name": "Acme Corp",
  "contact_person": "Alice",
  "contact_phone": "9876543210",
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
- **Response:** Same as create response

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
- **Request Body:** All fields optional
```json
{
  "business_name": "Updated Corp",
  "contact_person": "New Contact"
}
```
- **Response:** Same as create response

### Delete Business Owner
- **DELETE** `/business-owners/{owner_id}`
- **Note:** Cascades to delete all associated jobs and applications
- **Response:**
```json
{"detail": "Business owner deleted"}
```

---

## 👷 Workers

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
- **Validation Rules:**
  - Phone: 10-15 digits
  - Years of experience: 0-100
  - Email: Valid email format
  - User must exist in database
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
- **Response:** Same as create response

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
- **Request Body:** All fields optional
```json
{
  "name": "Updated Name",
  "skills": "New,Skills"
}
```
- **Response:** Same as create response

### Delete Worker
- **DELETE** `/workers/{worker_id}`
- **Note:** Cascades to delete all associated applications
- **Response:**
```json
{"detail": "Worker deleted"}
```

---

## 💼 Jobs

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
  "contact_phone": "9876543210",
  "contact_email": "alice@acme.com"
}
```
- **Validation Rules:**
  - Hourly rate: 0-10000
  - Estimated hours: 1-10000
  - Phone: 10-15 digits
  - Business owner must exist in database
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
  "contact_phone": "9876543210",
  "contact_email": "alice@acme.com",
  "posted_date": "2024-07-01T10:00:00",
  "status": "open"
}
```

### Get Job by ID
- **GET** `/jobs/{job_id}`
- **Response:** Same as create response

### Get All Jobs
- **GET** `/jobs/`
- **Response:**
```json
[
  { /* JobResponse */ }, ...
]
```

### Update Job
- **PUT** `/jobs/{job_id}`
- **Request Body:** All fields optional
```json
{
  "title": "Updated Job Title",
  "status": "closed"
}
```
- **Response:** Same as create response

### Delete Job
- **DELETE** `/jobs/{job_id}`
- **Note:** Cascades to delete all associated applications
- **Response:**
```json
{"detail": "Job deleted"}
```

---

## 📝 Job Applications

### Create Application
- **POST** `/applications/`
- **Request Body:**
```json
{
  "job_id": 1,
  "worker_id": 1,
  "message": "I am interested in this job."
}
```
- **Validation Rules:**
  - Job must exist in database
  - Worker must exist in database
- **Response:**
```json
{
  "id": 1,
  "job_id": 1,
  "worker_id": 1,
  "message": "I am interested in this job.",
  "status": "pending",
  "applied_date": "2024-07-01T11:00:00",
  "responded_date": null
}
```

### Get Application by ID
- **GET** `/applications/{application_id}`
- **Response:** Same as create response

### Get All Applications
- **GET** `/applications/`
- **Response:**
```json
[
  { /* JobApplicationResponse */ }, ...
]
```

### Update Application
- **PUT** `/applications/{application_id}`
- **Request Body:** All fields optional
```json
{
  "status": "accepted",
  "message": "Congratulations! You're hired."
}
```
- **Response:** Same as create response

### Delete Application
- **DELETE** `/applications/{application_id}`
- **Response:**
```json
{"detail": "Application deleted"}
```

---

## 🔒 Error Handling

### HTTP Status Codes
- **200**: Success
- **201**: Created
- **400**: Bad Request (validation errors)
- **401**: Unauthorized (invalid/missing JWT)
- **404**: Not Found (resource doesn't exist)
- **405**: Method Not Allowed
- **422**: Unprocessable Entity (validation errors)
- **500**: Internal Server Error

### Error Response Format
```json
{
  "detail": "Error message",
  "errors": [
    {
      "type": "value_error",
      "loc": ["body", "field_name"],
      "msg": "Validation error message",
      "input": "invalid_value"
    }
  ]
}
```

---

## 🧪 Testing

### Test Coverage
- **Total Test Cases**: 80
- **Success Rate**: 100%
- **Test Categories**:
  - CRUD operations for all entities
  - Edge cases and validation errors
  - Security tests (SQL injection, XSS)
  - Performance tests
  - Authentication tests

### Running Tests
```bash
# Local testing
python test/test_local.py

# Production testing
python test/test_vm.py
```

---

## 🔄 Deployment

### Production Environment
- **Platform**: Google Cloud Platform (GCP)
- **VM**: Debian 12
- **Domain**: myworkbee.duckdns.org
- **SSL**: Let's Encrypt certificate
- **Reverse Proxy**: Nginx
- **Database**: MySQL 8.0+

### CI/CD Pipeline
- **GitHub Actions**: Automated deployment
- **Trigger**: Push to main branch
- **Process**: SSH to GCP VM, pull code, restart service

### Manual Deployment
```bash
cd workbee-Back
git pull origin main
pkill -f uvicorn
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --daemon
```

---

## 📊 Database Schema

### Entity Relationships
- Users → Business Owners (1:1, cascade delete)
- Users → Workers (1:1, cascade delete)
- Business Owners → Jobs (1:many, cascade delete)
- Workers → Job Applications (1:many, cascade delete)
- Jobs → Job Applications (1:many, cascade delete)

### Foreign Key Constraints
- All relationships have proper foreign key constraints
- Cascade deletion ensures data integrity
- No orphaned records possible

---

## 🎯 Best Practices

### API Usage
1. **Always handle errors**: Check HTTP status codes
2. **Use proper authentication**: Include JWT tokens for protected endpoints
3. **Validate input**: Follow validation rules for all fields
4. **Handle pagination**: For large datasets (future enhancement)
5. **Use HTTPS**: All production requests should use HTTPS

### Development
1. **Test locally first**: Use `test_local.py` for development
2. **Check validation**: Ensure all input meets validation requirements
3. **Handle relationships**: Be aware of foreign key constraints
4. **Monitor logs**: Check server logs for detailed error information

---

## 📞 Support

For issues and questions:
- **Interactive Docs**: https://myworkbee.duckdns.org/docs
- **Test Examples**: Review test files for usage patterns
- **Server Logs**: Check application logs for detailed errors
- **Validation**: Ensure all input meets schema requirements 