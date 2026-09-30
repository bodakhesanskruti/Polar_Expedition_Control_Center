from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.database import get_db
from ..models import Inventory, Expedition
from ..schemas.inventory import InventoryCreate, InventoryOut, InventoryTransactionCreate
from ..services.inventory_service import low_stock, apply_transaction

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.get("", response_model=list[InventoryOut])
def list_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).order_by(Inventory.id).all()

@router.post("", response_model=InventoryOut, status_code=201)
def create_inventory(payload: InventoryCreate, db: Session = Depends(get_db)):
    if not db.get(Expedition, payload.expedition_id):
        raise HTTPException(404, "Expedition not found")
    item = Inventory(**payload.model_dump())
    item.status = "LOW" if item.quantity <= item.min_quantity else "AVAILABLE"
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/low-stock", response_model=list[InventoryOut])
def get_low_stock(db: Session = Depends(get_db)):
    return low_stock(db)

@router.post("/{inventory_id}/transactions", response_model=InventoryOut)
def inventory_transaction(inventory_id: int, payload: InventoryTransactionCreate, db: Session = Depends(get_db)):
    item = db.get(Inventory, inventory_id)
    if not item:
        raise HTTPException(404, "Inventory item not found")
    try:
        return apply_transaction(db, item, payload.transaction_type, payload.quantity, payload.remarks)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
