import os
from dotenv import load_dotenv
load_dotenv()  
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models  
from app.routers.application import router as application_router

app = FastAPI(title="Application Tracker API")


ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def startup_event():
    from app.scheduler import start_scheduler
    start_scheduler()


app.include_router(application_router)


@app.get("/")
def root():
    return {"message": "Application Tracker running"}
