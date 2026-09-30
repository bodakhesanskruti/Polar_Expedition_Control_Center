from datetime import datetime
from sqlalchemy.orm import Session
from ..models import Alert

def open_alerts(db: Session):
    return db.query(Alert).filter(Alert.status == "OPEN").order_by(Alert.created_at.desc()).all()

def create_alert(db: Session, **data):
    alert = Alert(**data)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

def resolve_alert(db: Session, alert_id: int):
    alert = db.get(Alert, alert_id)
    if not alert:
        return None
    alert.status = "RESOLVED"
    alert.resolved_at = datetime.utcnow()
    db.commit()
    db.refresh(alert)
    return alert
