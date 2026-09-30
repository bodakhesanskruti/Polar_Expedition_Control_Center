from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import Checkin, Personnel, Expedition
from pydantic import BaseModel

router = APIRouter(prefix="/checkins", tags=["Check-ins"])

class CheckinCreate(BaseModel):
    personnel_id: int
    expedition_id: int
    latitude: float
    longitude: float
    checkin_type: str = "ROUTINE"

@router.get("/status")
def status():
    return {"status": "MONITORING", "message": "Check-in monitoring endpoint is ready"}

@router.post("", status_code=201)
def create_checkin(payload: CheckinCreate, db: Session = Depends(get_db)):
    if not db.get(Personnel, payload.personnel_id):
        raise HTTPException(404, "Personnel not found")
    if not db.get(Expedition, payload.expedition_id):
        raise HTTPException(404, "Expedition not found")
    checkin = Checkin(**payload.model_dump())
    db.add(checkin)
    db.commit()
    db.refresh(checkin)
    return checkin

@router.get("/{personnel_id}")
def personnel_checkins(personnel_id: int, db: Session = Depends(get_db)):
    return db.query(Checkin).filter(Checkin.personnel_id == personnel_id).order_by(Checkin.checked_at.desc()).limit(50).all()
