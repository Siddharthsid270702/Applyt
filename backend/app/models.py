from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Boolean,
    ForeignKey,
    DateTime,
    Enum as SqlEnum
)
from sqlalchemy.orm import relationship
from datetime import date, datetime

from app.database import Base
from app.enums import ApplicationStatus


# =======================
# ACTIVE APPLICATIONS
# =======================
class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)

    # ── User isolation ──────────────────────────────────────────────────────
    user_id = Column(String(128), nullable=False, index=True)

    company = Column(String(255), nullable=False)
    role    = Column(String(255), nullable=False)

    status = Column(
        SqlEnum(ApplicationStatus),
        nullable=False,
        default=ApplicationStatus.APPLIED
    )

    source       = Column(String(100))
    applied_date = Column(Date, nullable=False, default=date.today)
    created_at   = Column(DateTime, default=datetime.utcnow)

    notes     = relationship("Note",     back_populates="application", cascade="all, delete-orphan")
    followups = relationship("FollowUp", back_populates="application", cascade="all, delete-orphan")


# =======================
# ARCHIVED APPLICATIONS
# =======================
class ArchivedApplication(Base):
    __tablename__ = "archived_applications"

    id = Column(Integer, primary_key=True, index=True)

    # ── User isolation ──────────────────────────────────────────────────────
    user_id = Column(String(128), nullable=False, index=True)

    company = Column(String(255), nullable=False)
    role    = Column(String(255), nullable=False)
    status  = Column(String(50),  nullable=False)

    source       = Column(String(100))
    applied_date = Column(Date)

    archive_reason = Column(String(50), nullable=False)
    archived_at    = Column(DateTime, default=datetime.utcnow)


# =======================
# NOTES
# =======================
class Note(Base):
    __tablename__ = "notes"

    id             = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"))
    note           = Column(Text, nullable=False)
    created_at     = Column(DateTime, default=datetime.utcnow)

    application = relationship("Application", back_populates="notes")


# =======================
# FOLLOW UPS
# =======================
class FollowUp(Base):
    __tablename__ = "followups"

    id             = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id", ondelete="CASCADE"))
    followup_date  = Column(Date, nullable=False)
    sent           = Column(Boolean, default=False)
    sent_at        = Column(DateTime, nullable=True)

    application = relationship("Application", back_populates="followups")
