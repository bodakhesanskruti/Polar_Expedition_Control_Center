from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import Expedition
from ..schemas.expedition import ExpeditionCreate, ExpeditionOut

router = APIRouter(prefix="/expeditions", tags=["Expeditions"])

@router.get("", response_model=list[ExpeditionOut])
def list_expeditions(db: Session = Depends(get_db)):
    return db.query(Expedition).order_by(Expedition.id.desc()).all()

@router.post("", response_model=ExpeditionOut, status_code=201)
def create_expedition(payload: ExpeditionCreate, db: Session = Depends(get_db)):
    if db.query(Expedition).filter(Expedition.code == payload.code).first():
        raise HTTPException(409, "Expedition code already exists")
    expedition = Expedition(**payload.model_dump())
    db.add(expedition)
    db.commit()
    db.refresh(expedition)
    return expedition

@router.get("/{expedition_id}", response_model=ExpeditionOut)
def get_expedition(expedition_id: int, db: Session = Depends(get_db)):
    expedition = db.get(Expedition, expedition_id)
    if not expedition:
        raise HTTPException(404, "Expedition not found")
    return expedition
