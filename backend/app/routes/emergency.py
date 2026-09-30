from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import EmergencyIncident, EmergencyResponse, Expedition, Personnel
from ..schemas.emergency import SOSCreate, IncidentOut, EmergencyResponseCreate
from ..services.alert_service import create_alert

router = APIRouter(prefix="/emergency", tags=["Emergency"])

@router.get("/incidents", response_model=list[IncidentOut])
def incidents(db: Session = Depends(get_db)):
    return db.query(EmergencyIncident).order_by(EmergencyIncident.created_at.desc()).limit(100).all()

@router.post("/sos", response_model=IncidentOut, status_code=201)
def sos(payload: SOSCreate, db: Session = Depends(get_db)):
    if not db.get(Expedition, payload.expedition_id):
        raise HTTPException(404, "Expedition not found")
    if payload.personnel_id is not None and not db.get(Personnel, payload.personnel_id):
        raise HTTPException(404, "Personnel not found")
    incident = EmergencyIncident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    create_alert(
        db,
        expedition_id=incident.expedition_id,
        personnel_id=incident.personnel_id,
        incident_id=incident.id,
        alert_type="EMERGENCY",
        severity=incident.severity,
        title=f"{incident.incident_type} - Emergency",
        message=incident.description,
    )
    return incident

@router.post("/incidents/{incident_id}/response")
def add_response(incident_id: int, payload: EmergencyResponseCreate, db: Session = Depends(get_db)):
    incident = db.get(EmergencyIncident, incident_id)
    if not incident:
        raise HTTPException(404, "Incident not found")
    response = EmergencyResponse(incident_id=incident_id, **payload.model_dump())
    incident.status = "IN_PROGRESS"
    db.add(response)
    db.commit()
    db.refresh(response)
    return response

@router.patch("/incidents/{incident_id}/resolve")
def resolve_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(EmergencyIncident, incident_id)
    if not incident:
        raise HTTPException(404, "Incident not found")
    incident.status = "RESOLVED"
    incident.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(incident)
    return incident
