import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE URL — reads from environment / .env
#
# LOCAL DEV (local Postgres):
#   DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/applyt
#
# PRODUCTION (Neon):
#   DATABASE_URL=postgresql+psycopg2://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
#   (Neon provides this string directly in their dashboard — just copy & paste)
# ─────────────────────────────────────────────────────────────────────────────

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:password@localhost:5432/applyt"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,    # auto-reconnect on dropped connections (important for Neon serverless)
    pool_recycle=300,      # recycle connections every 5 min (Neon sleeps idle connections)
    pool_size=5,           # keep a small pool — Neon free tier has connection limits
    max_overflow=2,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
