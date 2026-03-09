from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas

def create_application(db: Session, data: schemas.ApplicationCreate, user_id: str):
    app = models.Application(**data.model_dump(), user_id=user_id)
    db.add(app); db.commit(); db.refresh(app)
    return app

def get_active_applications(db: Session, user_id: str):
    return db.query(models.Application).filter(models.Application.user_id == user_id).all()

def get_archived_applications(db: Session, user_id: str):
    return db.query(models.ArchivedApplication).filter(models.ArchivedApplication.user_id == user_id).all()

def update_application(db: Session, app_id: int, update: schemas.ApplicationUpdate, user_id: str):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user_id).first()
    if not app: return None
    if update.status == "Rejected":
        archive_application(db, app, "Rejected", user_id); return None
    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(app, key, value)
    db.commit(); db.refresh(app)
    return app

def delete_application(db: Session, app_id: int, user_id: str):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user_id).first()
    if not app: return None
    archive_application(db, app, "Manually Deleted", user_id)
    return True

def archive_application(db: Session, app: models.Application, reason: str, user_id: str):
    archived = models.ArchivedApplication(
        user_id=user_id, company=app.company, role=app.role,
        status=app.status.value if hasattr(app.status, 'value') else str(app.status),
        source=app.source, applied_date=app.applied_date,
        archive_reason=reason, archived_at=datetime.utcnow()
    )
    db.add(archived); db.delete(app); db.commit()

def restore_application(db: Session, archived_id: int, user_id: str):
    archived = db.query(models.ArchivedApplication).filter(models.ArchivedApplication.id == archived_id, models.ArchivedApplication.user_id == user_id).first()
    if not archived: return None
    app = models.Application(user_id=user_id, company=archived.company, role=archived.role, status="Applied", source=archived.source, applied_date=archived.applied_date)
    db.add(app); db.delete(archived); db.commit(); db.refresh(app)
    return app

def add_note(db: Session, app_id: int, note_data: schemas.NoteCreate, user_id: str):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user_id).first()
    if not app: return None
    note = models.Note(application_id=app_id, note=note_data.note)
    db.add(note); db.commit(); db.refresh(note)
    return note

def get_notes(db: Session, app_id: int, user_id: str):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user_id).first()
    if not app: return []
    return db.query(models.Note).filter(models.Note.application_id == app_id).all()

def add_followup(db: Session, app_id: int, followup_data: schemas.FollowUpCreate, user_id: str):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user_id).first()
    if not app: return None
    followup = models.FollowUp(application_id=app_id, followup_date=followup_data.followup_date)
    db.add(followup); db.commit(); db.refresh(followup)
    return followup

def get_followups(db: Session, app_id: int, user_id: str):
    app = db.query(models.Application).filter(models.Application.id == app_id, models.Application.user_id == user_id).first()
    if not app: return []
    return db.query(models.FollowUp).filter(models.FollowUp.application_id == app_id).all()

def mark_followup_sent(db: Session, followup_id: int, user_id: str):
    followup = (
        db.query(models.FollowUp)
        .join(models.Application)
        .filter(models.FollowUp.id == followup_id, models.Application.user_id == user_id)
        .first()
    )
    if not followup: return None
    followup.sent = True; followup.sent_at = datetime.utcnow()
    db.commit(); db.refresh(followup)
    return followup
