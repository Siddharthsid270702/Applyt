from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud, schemas
from app.auth import get_current_user

router = APIRouter(prefix="/applications", tags=["Applications"])

# =======================
# FOLLOW UPS — must be defined BEFORE /{app_id} routes
# to avoid FastAPI matching "followups" as an app_id
# =======================
@router.put("/followups/{followup_id}/sent", response_model=schemas.FollowUpOut)
def mark_followup_sent(
    followup_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    result = crud.mark_followup_sent(db, followup_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return result


# =======================
# ARCHIVE — must be defined BEFORE /{app_id} routes
# =======================
@router.get("/archived", response_model=List[schemas.ArchivedApplicationOut])
def archived_applications(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return crud.get_archived_applications(db, user_id)


@router.post("/archived/{archived_id}/restore")
def restore_archived_application(
    archived_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    restored = crud.restore_application(db, archived_id, user_id)
    if not restored:
        raise HTTPException(status_code=404, detail="Archived application not found")
    return {"message": "Application restored successfully"}


# =======================
# APPLICATION
# =======================
@router.post("/", response_model=schemas.ApplicationOut)
def create_application(
    data: schemas.ApplicationCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return crud.create_application(db, data, user_id)


@router.get("/", response_model=List[schemas.ApplicationOut])
def get_applications(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return crud.get_active_applications(db, user_id)


@router.put("/{app_id}")
def update_application(
    app_id: int,
    update: schemas.ApplicationUpdate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    result = crud.update_application(db, app_id, update, user_id)

    if result is None and update.status == "Rejected":
        return {"message": "Application rejected and archived"}

    if not result:
        raise HTTPException(status_code=404, detail="Application not found")

    return result


@router.delete("/{app_id}")
def delete_application(
    app_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    success = crud.delete_application(db, app_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"message": "Application archived successfully"}


# =======================
# NOTES
# =======================
@router.post("/{app_id}/notes", response_model=schemas.NoteOut)
def create_note(
    app_id: int,
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    result = crud.add_note(db, app_id, note, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")
    return result


@router.get("/{app_id}/notes", response_model=List[schemas.NoteOut])
def list_notes(
    app_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return crud.get_notes(db, app_id, user_id)


# =======================
# FOLLOW UPS (per application)
# =======================
@router.post("/{app_id}/followups", response_model=schemas.FollowUpOut)
def create_followup(
    app_id: int,
    followup: schemas.FollowUpCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    result = crud.add_followup(db, app_id, followup, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Application not found")
    return result


@router.get("/{app_id}/followups", response_model=List[schemas.FollowUpOut])
def list_followups(
    app_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return crud.get_followups(db, app_id, user_id)
