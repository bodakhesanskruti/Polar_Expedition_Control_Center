from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import Personnel, Team
from ..schemas.personnel import PersonnelCreate, PersonnelOut

router = APIRouter(prefix="/personnel", tags=["Personnel"])

@router.get("", response_model=list[PersonnelOut])
def list_personnel(db: Session = Depends(get_db)):
    return db.query(Personnel).order_by(Personnel.id).all()

@router.post("", response_model=PersonnelOut, status_code=201)
def create_personnel(payload: PersonnelCreate, db: Session = Depends(get_db)):
    if payload.team_id is not None and not db.get(Team, payload.team_id):
        raise HTTPException(404, "Team not found")
    person = Personnel(**payload.model_dump())
    db.add(person)
    db.commit()
    db.refresh(person)
    return person

@router.get("/{personnel_id}", response_model=PersonnelOut)
def get_personnel(personnel_id: int, db: Session = Depends(get_db)):
    person = db.get(Personnel, personnel_id)
    if not person:
        raise HTTPException(404, "Personnel not found")
    return person
