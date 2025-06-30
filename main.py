from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
# Import all models so SQLAlchemy knows about them
from models.user import User
from models.business_owner import BusinessOwner
from models.worker import Worker
from models.job import Job
from models.job_application import JobApplication
from api import user_routes, business_owner_routes, worker_routes, job_routes, application_routes

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.router)
app.include_router(business_owner_routes.router)
app.include_router(worker_routes.router)
app.include_router(job_routes.router)
app.include_router(application_routes.router) 