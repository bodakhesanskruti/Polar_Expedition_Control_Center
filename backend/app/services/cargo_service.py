from sqlalchemy.orm import Session
from ..models import CargoTracking

def latest_tracking(db: Session, cargo_id: int):
    return db.query(CargoTracking).filter(
        CargoTracking.cargo_id == cargo_id
    ).order_by(CargoTracking.recorded_at.desc()).first()

def latest_points(db: Session, limit: int = 100):
    rows = db.query(CargoTracking).order_by(CargoTracking.recorded_at.desc()).limit(limit).all()
    seen = set()
    result = []
    for row in rows:
        if row.cargo_id in seen:
            continue
        seen.add(row.cargo_id)
        result.append(row)
    return result
