from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    expedition_id: int
    personnel_id: int | None
    cargo_id: int | None
    inventory_id: int | None
    incident_id: int | None
    alert_type: str
    severity: str
    title: str
    message: str
    status: str
    created_at: datetime
    resolved_at: datetime | None
