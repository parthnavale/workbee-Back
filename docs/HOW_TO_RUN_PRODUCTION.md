# How to Run Workbee Backend in Production

This guide explains how to deploy the Workbee FastAPI backend for production use.

---

## 1. Install Dependencies

Activate your virtual environment and install production dependencies:
```bash
source workbee-Back/venv/bin/activate
pip install gunicorn uvicorn
```

## 2. Set Environment Variables

Set environment variables for security and configuration (example for Linux):
```bash
export WORKBEE_SECRET_KEY="your-very-secret-key"
export WORKBEE_DATABASE_URL="sqlite:///./workbee.db"  # Or your production DB URL
```

## 3. Run with Gunicorn and Uvicorn Workers

Start the server with Gunicorn and Uvicorn workers:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker workbee-Back.main:app --bind 0.0.0.0:8000
```
- `-w 4` sets 4 worker processes (adjust for your CPU)
- `--bind 0.0.0.0:8000` makes the app accessible on all interfaces

## 4. Use a Process Manager (Recommended)

For automatic restarts and monitoring, use a process manager like `systemd`, `supervisor`, or `pm2`.

## 5. Set Up a Reverse Proxy (Recommended)

Use Nginx, Caddy, or Apache as a reverse proxy for:
- SSL/TLS termination (HTTPS)
- Compression
- Security headers
- Serving static files

Example Nginx config:
```
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 6. CORS & Security
- Adjust CORS settings in `main.py` to allow only your frontend domain.
- Set strong, unique secrets for JWT and database.

## 7. Logs & Monitoring
- Monitor Gunicorn and process manager logs.
- Set up alerts for errors and downtime.

## Database Migrations with Alembic

For production, use Alembic to manage database schema changes instead of Base.metadata.create_all.

### 1. Install Alembic
```bash
pip install alembic
```

### 2. Initialize Alembic in your project root
```bash
alembic init alembic
```

### 3. Configure Alembic
- Edit `alembic.ini` and set `sqlalchemy.url` to your WORKBEE_DATABASE_URL or use env var substitution.
- In `alembic/env.py`, import your models:
  ```python
  from models.user import User
  from models.business_owner import BusinessOwner
  from models.worker import Worker
  from models.job import Job
  from models.job_application import JobApplication
  from core.database import Base
  target_metadata = Base.metadata
  ```

### 4. Create and Apply Migrations
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

- Repeat for future schema changes.

---

For more, see the [FastAPI deployment docs](https://fastapi.tiangolo.com/deployment/). 