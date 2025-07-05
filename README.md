# Workbee Backend API

A FastAPI-based backend for the Workbee job marketplace platform, providing comprehensive CRUD operations for users, business owners, workers, jobs, and job applications.

## 🚀 Features

- **User Management**: Registration, authentication, and profile management
- **Business Owner Management**: Company profiles and job posting capabilities
- **Worker Management**: Professional profiles and skill management
- **Job Management**: Job posting, searching, and management
- **Application System**: Job application and status tracking
- **JWT Authentication**: Secure token-based authentication
- **MySQL Database**: Production-ready database with proper relationships
- **Cascade Deletion**: Proper data integrity with foreign key constraints

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Validation**: Pydantic
- **Documentation**: Auto-generated OpenAPI/Swagger

## 📋 Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

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

### 6. Initialize Database Tables
```bash
python create_tables.py
```

## 🚀 Running the Application

### Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: `POST /users/register`
2. **Login**: `POST /users/login`
3. **Use Token**: Include `Authorization: Bearer <token>` in request headers

## 📊 Database Schema

### Core Entities
- **Users**: Base user accounts with roles (poster/seeker)
- **Business Owners**: Company profiles linked to users
- **Workers**: Professional profiles linked to users
- **Jobs**: Job postings by business owners
- **Job Applications**: Applications by workers for jobs

### Relationships
- Users → Business Owners (1:1)
- Users → Workers (1:1)
- Business Owners → Jobs (1:many)
- Workers → Job Applications (1:many)
- Jobs → Job Applications (1:many)

## 🗑️ Data Deletion

The API implements proper cascade deletion:
- Deleting a business owner removes all associated jobs and applications
- Deleting a worker removes all associated applications
- Deleting a job removes all associated applications
- Users can only be deleted after removing associated profiles

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Environment variable configuration
- Input validation with Pydantic
- SQL injection protection via SQLAlchemy

## 🐳 Docker Deployment

Build and run with Docker:
```bash
docker build -t workbee-backend .
docker run -p 8000:8000 workbee-backend
```

## 📁 Project Structure

```
workbee-Back/
├── api/                    # API route handlers
│   ├── auth.py            # JWT authentication
│   ├── user_routes.py     # User management
│   ├── business_owner_routes.py
│   ├── worker_routes.py
│   ├── job_routes.py
│   └── application_routes.py
├── core/                   # Core functionality
│   └── database.py        # Database configuration
├── models/                 # SQLAlchemy models
├── schemas/                # Pydantic schemas
├── docs/                   # Documentation
├── main.py                # FastAPI application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
└── example.env           # Environment template
```

## 🧪 Testing

The API includes comprehensive CRUD operations for all entities. Test endpoints using the interactive documentation at `/docs`.

## 📝 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | MySQL connection string | Yes | - |
| `WORKBEE_SECRET_KEY` | JWT secret key | Yes | workbee_secret |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions, please refer to the documentation in the `docs/` directory or create an issue in the repository. 