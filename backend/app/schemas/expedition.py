from datetime import datetime
from pydantic import BaseModel, ConfigDict

class ExpeditionCreate(BaseModel):
    name: str
    code: str
    destination: str
    status: str = "PLANNED"
    start_date: datetime | None = None
    end_date: datetime | None = None

class ExpeditionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    code: str
    destination: str
    status: str
    start_date: datetime | None
    end_date: datetime | None
