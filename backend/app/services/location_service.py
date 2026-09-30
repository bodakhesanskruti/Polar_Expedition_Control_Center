from sqlalchemy.orm import Session
from ..models import CargoTracking, PersonnelLocation
from .cargo_service import latest_points

def live_points(db: Session):
    cargo_points = latest_points(db)
    personnel_rows = db.query(PersonnelLocation).order_by(PersonnelLocation.recorded_at.desc()).limit(100).all()
    seen = set()
    personnel_points = []
    for row in personnel_rows:
        if row.personnel_id in seen:
            continue
        seen.add(row.personnel_id)
        personnel_points.append(row)
    return cargo_points, personnel_points
