from pydantic import BaseModel, ConfigDict

class PersonnelCreate(BaseModel):
    name: str
    role: str
    phone: str | None = None
    status: str = "ACTIVE"
    team_id: int | None = None

class PersonnelOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    role: str
    phone: str | None
    status: str
    team_id: int | None

class PersonnelLocationCreate(BaseModel):
    personnel_id: int
    expedition_id: int
    latitude: float
    longitude: float
    status: str = "MOVING"
