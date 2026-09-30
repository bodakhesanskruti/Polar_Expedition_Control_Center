from sqlalchemy.orm import Session
from ..models import Inventory, InventoryTransaction

def low_stock(db: Session):
    return db.query(Inventory).filter(Inventory.quantity <= Inventory.min_quantity).all()

def apply_transaction(db: Session, inventory: Inventory, transaction_type: str, quantity: float, remarks: str | None):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
    transaction_type = transaction_type.upper()
    if transaction_type == "IN":
        inventory.quantity += quantity
    elif transaction_type == "OUT":
        if inventory.quantity < quantity:
            raise ValueError("Insufficient inventory")
        inventory.quantity -= quantity
    else:
        raise ValueError("transaction_type must be IN or OUT")
    inventory.status = "LOW" if inventory.quantity <= inventory.min_quantity else "AVAILABLE"
    tx = InventoryTransaction(
        inventory_id=inventory.id,
        expedition_id=inventory.expedition_id,
        transaction_type=transaction_type,
        quantity=quantity,
        remarks=remarks,
    )
    db.add(tx)
    db.commit()
    db.refresh(inventory)
    return inventory
