from datetime import datetime
from pydantic import BaseModel, ConfigDict

class SOSCreate(BaseModel):
    expedition_id: int
    personnel_id: int | None = None
    incident_type: str = "SOS"
    severity: str = "HIGH"
    description: str = "Emergency SOS triggered"
    latitude: float | None = None
    longitude: float | None = None

class IncidentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    expedition_id: int
    personnel_id: int | None
    incident_type: str
    severity: str
    description: str
    latitude: float | None
    longitude: float | None
    status: str
    created_at: datetime
    resolved_at: datetime | None

class EmergencyResponseCreate(BaseModel):
    responder: str
    action: str
    status: str = "ASSIGNED"
