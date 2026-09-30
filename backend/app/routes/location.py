from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import PersonnelLocation, Personnel, Expedition
from ..schemas.personnel import PersonnelLocationCreate
from ..services.location_service import live_points

router = APIRouter(prefix="/locations", tags=["Locations"])

@router.get("/live")
def live(db: Session = Depends(get_db)):
    cargo, personnel = live_points(db)
    return {
        "cargo": [
            {"cargo_id": x.cargo_id, "latitude": x.latitude, "longitude": x.longitude, "status": x.status, "mode": x.transport_mode, "recorded_at": x.recorded_at}
            for x in cargo
        ],
        "personnel": [
            {"personnel_id": x.personnel_id, "expedition_id": x.expedition_id, "latitude": x.latitude, "longitude": x.longitude, "status": x.status, "recorded_at": x.recorded_at}
            for x in personnel
        ],
    }

@router.post("/personnel", status_code=201)
def add_personnel_location(payload: PersonnelLocationCreate, db: Session = Depends(get_db)):
    if not db.get(Personnel, payload.personnel_id):
        raise HTTPException(404, "Personnel not found")
    if not db.get(Expedition, payload.expedition_id):
        raise HTTPException(404, "Expedition not found")
    row = PersonnelLocation(**payload.model_dump())
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
