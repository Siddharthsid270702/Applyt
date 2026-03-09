import os
from dotenv import load_dotenv
load_dotenv()  # ← loads .env file automatically before anything else

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models  # DO NOT REMOVE — needed to register models with Base
from app.routers.application import router as application_router

app = FastAPI(title="Application Tracker API")

# ✅ FIXED: CORS now reads allowed origins from env variable for production
# In dev: set ALLOWED_ORIGINS="http://localhost:5173"
# In prod: set ALLOWED_ORIGINS="https://your-frontend.vercel.app"
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

# Create tables on startup
Base.metadata.create_all(bind=engine)

# ✅ FIXED: Scheduler now started properly via lifespan event, not at module level
# (module-level scheduler.start() would run during import, causing issues in prod)
@app.on_event("startup")
def startup_event():
    from app.scheduler import start_scheduler
    start_scheduler()

# Routers
app.include_router(application_router)


@app.get("/")
def root():
    return {"message": "Application Tracker running"}
