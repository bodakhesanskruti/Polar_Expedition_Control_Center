from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class AlertCreate(BaseModel):
    expedition_id: int
    alert_type: str
    severity: str = "MEDIUM"
    title: str
    message: str
    personnel_id: int | None = None
    cargo_id: int | None = None
    inventory_id: int | None = None
    incident_id: int | None = None

class DashboardStats(BaseModel):
    active_expeditions: int
    active_personnel: int
    cargo_in_transit: int
    open_alerts: int
    low_stock_items: int
    open_emergencies: int

class Health(BaseModel):
    status: str
    database: str
    timestamp: datetime
