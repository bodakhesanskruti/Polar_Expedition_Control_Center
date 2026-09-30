from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CargoCreate(BaseModel):
    expedition_id: int
    tracking_code: str
    description: str
    weight_kg: float = 0
    status: str = "PLANNED"
    priority: str = "NORMAL"

class CargoStatusUpdate(BaseModel):
    status: str

class CargoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    expedition_id: int
    tracking_code: str
    description: str
    weight_kg: float
    status: str
    priority: str

class TrackingCreate(BaseModel):
    cargo_id: int
    expedition_id: int
    location_id: int | None = None
    latitude: float
    longitude: float
    transport_mode: str = "VEHICLE"
    status: str = "IN_TRANSIT"

class TrackingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cargo_id: int
    expedition_id: int
    latitude: float
    longitude: float
    transport_mode: str
    status: str
    recorded_at: datetime
