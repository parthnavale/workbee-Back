# Workbee Backend API

A production-ready FastAPI-based backend for the Workbee job marketplace platform, providing comprehensive CRUD operations for users, business owners, workers, jobs, and job applications with real-time WebSocket notifications, full test coverage and deployment automation.

## 🚀 Production Status

✅ **Fully Deployed**: Running on GCP VM with HTTPS  
✅ **Domain**: https://myworkbee.duckdns.org  
✅ **WebSocket**: Real-time notifications via WSS  
✅ **Test Coverage**: 100% success rate (80 test cases)  
✅ **Database**: MySQL with proper relationships and constraints  
✅ **Security**: JWT authentication, input validation, SQL injection protection  
✅ **Documentation**: Auto-generated OpenAPI/Swagger at `/docs`  

## 🎯 Features

- **Complete User Management**: Registration, authentication, profile management with role-based access
- **Business Owner Management**: Company profiles with validation (phone, year, etc.)
- **Worker Management**: Professional profiles with skills and experience tracking
- **Job Management**: Comprehensive job posting with location, rates, and requirements
- **Application System**: Full application lifecycle with status tracking and messaging
- **Real-time Notifications**: WebSocket-based notifications for job applications and status updates
- **JWT Authentication**: Secure token-based authentication with proper error handling
- **MySQL Database**: Production-ready database with foreign key constraints and cascade deletion
- **Input Validation**: Comprehensive validation for all fields (phone numbers, emails, years, etc.)
- **Error Handling**: Proper HTTP status codes and JSON error responses
- **CORS Support**: Cross-origin resource sharing enabled
- **Performance Optimized**: Efficient database queries and response handling

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.115.14
- **Database**: MySQL 8.0+ with mysql-connector-python
- **ORM**: SQLAlchemy 2.0.41
- **Authentication**: JWT with python-jose[cryptography]
- **Password Hashing**: bcrypt 4.0.1
- **Validation**: Pydantic 2.11.7 with custom validators
- **Real-time**: WebSocket support for notifications
- **Documentation**: Auto-generated OpenAPI/Swagger
- **Deployment**: GCP VM with Nginx reverse proxy and Let's Encrypt SSL

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)
- GCP VM (for production deployment)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd workbee-Back
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Copy the example environment file and configure your settings:
```bash
cp example.env .env
```

Edit `.env` with your production values:
```env
# Database Configuration
DATABASE_URL=mysql+mysqlconnector://username:password@localhost:3306/workbee_db

# JWT Configuration
WORKBEE_SECRET_KEY=your-very-secure-secret-key-here

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 5. Database Setup
Create the MySQL database and user:
```sql
CREATE DATABASE workbee_db;
CREATE USER 'workbee_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON workbee_db.* TO 'workbee_user'@'localhost';
FLUSH PRIVILEGES;
```

### 6. Database Migration
Use Alembic for database migrations:
```bash
# Initialize Alembic (first time only)
alembic init alembic

# Create a new migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## 🚀 Running the Application

### Development Mode
```bash
cd workbee-Back
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
cd workbee-Back
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 Production Deployment

### GCP VM Setup
1. **Create VM**: Debian 12 with appropriate resources
2. **Install Dependencies**: Python, MySQL, Nginx
3. **Configure Nginx**: Reverse proxy to FastAPI on port 8000
4. **SSL Certificate**: Let's Encrypt with DuckDNS domain
5. **Firewall**: Open ports 80, 443, 22
6. **WebSocket Support**: Configure Nginx for WebSocket upgrade

### Domain Configuration
- **Domain**: myworkbee.duckdns.org
- **SSL**: Let's Encrypt certificate (auto-renewal)
- **Nginx**: Reverse proxy configuration with WebSocket support
- **WebSocket**: WSS endpoint at `/ws/notifications/{user_id}`

### GitHub Actions Deployment
Automated deployment pipeline:
- Code push triggers deployment
- SSH connection to GCP VM
- Service restart without dependency reinstallation
- Zero-downtime deployments

## 📚 API Documentation

Access the interactive API documentation:

- **Production**: https://myworkbee.duckdns.org/docs
- **Local**: http://localhost:8000/docs
- **ReDoc**: https://myworkbee.duckdns.org/redoc
- **OpenAPI JSON**: https://myworkbee.duckdns.org/openapi.json

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /users/register`
2. **Login**: `POST /users/login`
3. **Use Token**: Include `Authorization: Bearer <token>` in request headers
4. **Protected Endpoints**: `/users/me`, business owner, worker, job, and application management

## 🔌 Real-time Notifications

### WebSocket Endpoints
- **Worker Notifications**: `wss://myworkbee.duckdns.org/ws/notifications/{worker_id}`
- **Business Owner Notifications**: `wss://myworkbee.duckdns.org/ws/notifications/{business_owner_id}`

### Notification Types
- **New Job Application**: Sent to business owners when workers apply
- **Application Status Update**: Sent to workers when applications are accepted/rejected
- **Job Status Changes**: Real-time updates for job status modifications

### WebSocket Connection
```javascript
// Example WebSocket connection
const ws = new WebSocket(`wss://myworkbee.duckdns.org/ws/notifications/${userId}`);

ws.onmessage = function(event) {
    const notification = JSON.parse(event.data);
    console.log('New notification:', notification);
};

ws.onclose = function() {
    console.log('WebSocket connection closed');
};
```

## 📊 Database Schema

### Core Entities
- **Users**: Base user accounts with roles (poster/seeker)
- **Business Owners**: Company profiles linked to users
- **Workers**: Professional profiles linked to users
- **Jobs**: Job postings by business owners
- **Job Applications**: Applications by workers for jobs

### Relationships & Constraints
- Users → Business Owners (1:1, cascade delete)
- Users → Workers (1:1, cascade delete)
- Business Owners → Jobs (1:many, cascade delete)
- Workers → Job Applications (1:many, cascade delete)
- Jobs → Job Applications (1:many, cascade delete)

### Validation Rules
- **Phone Numbers**: 10-15 digits, Indian numbers start with 6,7,8,9
- **Years**: Between 1800-2100 for business establishment
- **Emails**: Valid email format validation
- **Usernames**: Alphanumeric with underscores only
- **Passwords**: Minimum length and complexity requirements

## 🗑️ Data Deletion & Integrity

The API implements proper cascade deletion:
- Deleting a business owner removes all associated jobs and applications
- Deleting a worker removes all associated applications
- Deleting a job removes all associated applications
- Users can only be deleted after removing associated profiles
- Foreign key constraints prevent orphaned data

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Authentication**: Secure token-based auth with expiration
- **Environment Variables**: No hardcoded secrets
- **Input Validation**: Pydantic schemas with custom validators
- **SQL Injection Protection**: SQLAlchemy ORM
- **CORS Configuration**: Proper cross-origin handling
- **Error Handling**: Secure error messages without data leakage
- **WebSocket Security**: Authentication and validation for real-time connections

## 🧪 Testing

### Comprehensive Test Coverage
- **Total Test Cases**: 80
- **Success Rate**: 100%
- **Test Types**: CRUD operations, edge cases, security, performance, WebSocket

### Test Categories
- **User Management**: Registration, login, profile updates
- **Business Owner Operations**: CRUD operations with validation
- **Worker Operations**: Profile management and skills tracking
- **Job Management**: Posting, updating, status changes
- **Application System**: Apply, respond, status tracking
- **Authentication**: JWT token validation and security
- **WebSocket**: Real-time notification testing
- **Error Handling**: Invalid inputs and edge cases
- **Performance**: Database query optimization

### Running Tests
```bash
# Run all tests
python -m pytest test/

# Run specific test file
python -m pytest test/test_local.py

# Run with verbose output
python -m pytest -v test/
```

## 📈 Performance & Monitoring

### Database Optimization
- **Indexed Queries**: Proper indexing on frequently queried fields
- **Efficient Joins**: Optimized database relationships
- **Connection Pooling**: SQLAlchemy connection management
- **Query Optimization**: Minimal database round trips

### API Performance
- **Response Times**: < 200ms for most operations
- **Concurrent Users**: Supports multiple simultaneous connections
- **WebSocket Scaling**: Efficient real-time communication
- **Memory Usage**: Optimized for production workloads

## 🔄 API Endpoints

### Authentication
- `POST /users/register` - User registration
- `POST /users/login` - User login
- `GET /users/me` - Get current user profile

### Business Owners
- `POST /business-owners/` - Create business owner profile
- `GET /business-owners/{id}` - Get business owner details
- `PUT /business-owners/{id}` - Update business owner profile
- `DELETE /business-owners/{id}` - Delete business owner

### Workers
- `POST /workers/` - Create worker profile
- `GET /workers/{id}` - Get worker details
- `PUT /workers/{id}` - Update worker profile
- `DELETE /workers/{id}` - Delete worker

### Jobs
- `POST /jobs/` - Create new job posting
- `GET /jobs/` - Get all jobs (with filtering)
- `GET /jobs/{id}` - Get specific job details
- `PUT /jobs/{id}` - Update job posting
- `DELETE /jobs/{id}` - Delete job posting

### Applications
- `POST /applications/` - Apply for a job
- `GET /applications/` - Get all applications
- `GET /applications/{id}` - Get specific application
- `PUT /applications/{id}` - Update application status
- `DELETE /applications/{id}` - Delete application

### WebSocket
- `WS /ws/notifications/{user_id}` - Real-time notifications

## 🚀 Deployment Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] SSL certificates installed
- [ ] Nginx configuration updated
- [ ] Firewall rules configured
- [ ] Monitoring setup complete

### Post-deployment
- [ ] API endpoints tested
- [ ] WebSocket connections verified
- [ ] Database connections stable
- [ ] Error logging configured
- [ ] Performance monitoring active
- [ ] Backup system operational

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Update documentation
6. Submit a pull request

### Development Guidelines
- Follow PEP 8 style guidelines
- Add comprehensive tests
- Update API documentation
- Use type hints
- Handle errors gracefully

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation at `/docs`
- Review the deployment guides in `/docs`

---

**Workbee Backend** - Powering the future of job matching! 🚀 