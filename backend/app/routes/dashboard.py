from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database.database import get_db
from ..models import Expedition, Personnel, Cargo, Inventory, Alert, EmergencyIncident
from ..schemas.common import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=DashboardStats)
def stats(db: Session = Depends(get_db)):
    return DashboardStats(
        active_expeditions=db.query(Expedition).filter(Expedition.status.in_(["ACTIVE", "IN_PROGRESS"])).count(),
        active_personnel=db.query(Personnel).filter(Personnel.status == "ACTIVE").count(),
        cargo_in_transit=db.query(Cargo).filter(Cargo.status.in_(["IN_TRANSIT", "PICKED_UP", "IN_TRANSIT "])).count(),
        open_alerts=db.query(Alert).filter(Alert.status == "OPEN").count(),
        low_stock_items=db.query(Inventory).filter(Inventory.quantity <= Inventory.min_quantity).count(),
        open_emergencies=db.query(EmergencyIncident).filter(EmergencyIncident.status.in_(["OPEN", "IN_PROGRESS"])).count(),
    )
