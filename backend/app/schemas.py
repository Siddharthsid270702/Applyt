from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ApplicationBase(BaseModel):
    company: str
    role: str
    status: str
    source: Optional[str] = None
    applied_date: date = None

    def model_post_init(self, __context):
        if self.applied_date is None:
            self.applied_date = date.today()

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None
    source: Optional[str] = None
    applied_date: Optional[date] = None

class ApplicationOut(ApplicationBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    note: str

class NoteOut(BaseModel):
    id: int
    note: str
    created_at: datetime
    class Config:
        from_attributes = True

class FollowUpCreate(BaseModel):
    followup_date: date

class FollowUpOut(BaseModel):
    id: int
    followup_date: date
    sent: bool
    sent_at: Optional[datetime] = None
    class Config:
        from_attributes = True

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
