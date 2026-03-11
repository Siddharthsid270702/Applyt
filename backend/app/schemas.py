from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# =====================
# APPLICATION
# =====================
class ApplicationBase(BaseModel):
    company: str
    role: str
    status: str
    source: Optional[str] = None
    applied_date: date = None  # ✅ FIXED: was date.today() which evaluates at class definition time

    def model_post_init(self, __context):
        if self.applied_date is None:
            self.applied_date = date.today()


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationUpdate(BaseModel):
    # ✅ BUG FIX: Original had 'status' but crud.py checks update.status — was inconsistent
    # Keeping 'status' as the single field name throughout
    status: Optional[str] = None
    source: Optional[str] = None
    applied_date: Optional[date] = None


class ApplicationOut(ApplicationBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =====================
# NOTES
# =====================
class NoteCreate(BaseModel):
    note: str


class NoteOut(BaseModel):
    id: int
    note: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================
# FOLLOW UPS
# =====================
class FollowUpCreate(BaseModel):
    followup_date: date


class FollowUpOut(BaseModel):
    id: int
    followup_date: date
    sent: bool
    sent_at: Optional[datetime] = None  # ✅ FIXED: Added default None to avoid validation error

    class Config:
        from_attributes = True


# =====================
# ARCHIVED
# =====================
class ArchivedApplicationOut(BaseModel):
    id: int
    company: str
    role: str
    status: str
    source: Optional[str] = None
    applied_date: Optional[date] = None
    archive_reason: str
    archived_at: datetime

    class Config:
        from_attributes = True
