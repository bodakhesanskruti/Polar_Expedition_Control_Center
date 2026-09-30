from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import Cargo, CargoTracking, Expedition
from ..schemas.cargo import CargoCreate, CargoOut, CargoStatusUpdate, TrackingCreate, TrackingOut
from ..services.cargo_service import latest_tracking, latest_points

router = APIRouter(prefix="/cargo", tags=["Cargo"])

@router.get("", response_model=list[CargoOut])
def list_cargo(db: Session = Depends(get_db)):
    return db.query(Cargo).order_by(Cargo.id.desc()).all()

@router.post("", response_model=CargoOut, status_code=201)
def create_cargo(payload: CargoCreate, db: Session = Depends(get_db)):
    if not db.get(Expedition, payload.expedition_id):
        raise HTTPException(404, "Expedition not found")
    if db.query(Cargo).filter(Cargo.tracking_code == payload.tracking_code).first():
        raise HTTPException(409, "Tracking code already exists")
    cargo = Cargo(**payload.model_dump())
    db.add(cargo)
    db.commit()
    db.refresh(cargo)
    return cargo

@router.patch("/{cargo_id}/status", response_model=CargoOut)
def update_status(cargo_id: int, payload: CargoStatusUpdate, db: Session = Depends(get_db)):
    cargo = db.get(Cargo, cargo_id)
    if not cargo:
        raise HTTPException(404, "Cargo not found")
    cargo.status = payload.status.upper()
    db.commit()
    db.refresh(cargo)
    return cargo

@router.get("/{cargo_id}/tracking", response_model=TrackingOut | None)
def cargo_tracking(cargo_id: int, db: Session = Depends(get_db)):
    if not db.get(Cargo, cargo_id):
        raise HTTPException(404, "Cargo not found")
    return latest_tracking(db, cargo_id)

@router.post("/tracking", response_model=TrackingOut, status_code=201)
def add_tracking(payload: TrackingCreate, db: Session = Depends(get_db)):
    cargo = db.get(Cargo, payload.cargo_id)
    if not cargo:
        raise HTTPException(404, "Cargo not found")
    tracking = CargoTracking(**payload.model_dump())
    cargo.status = payload.status.upper()
    db.add(tracking)
    db.commit()
    db.refresh(tracking)
    return tracking

@router.get("/tracking", response_model=list[TrackingOut])
def tracking(db: Session = Depends(get_db)):
    return latest_points(db)
