from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import Alert
from ..schemas.alert import AlertOut
from ..schemas.common import AlertCreate
from ..services.alert_service import open_alerts, create_alert, resolve_alert

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=list[AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.created_at.desc()).limit(100).all()

@router.get("/open", response_model=list[AlertOut])
def list_open_alerts(db: Session = Depends(get_db)):
    return open_alerts(db)

@router.post("", response_model=AlertOut, status_code=201)
def add_alert(payload: AlertCreate, db: Session = Depends(get_db)):
    return create_alert(db, **payload.model_dump())

@router.patch("/{alert_id}/resolve", response_model=AlertOut)
def resolve(alert_id: int, db: Session = Depends(get_db)):
    alert = resolve_alert(db, alert_id)
    if not alert:
        raise HTTPException(404, "Alert not found")
    return alert
