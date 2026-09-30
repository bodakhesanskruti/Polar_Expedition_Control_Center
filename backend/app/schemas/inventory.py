from pydantic import BaseModel, ConfigDict

class InventoryCreate(BaseModel):
    expedition_id: int
    item_name: str
    category: str
    quantity: float
    unit: str = "units"
    min_quantity: float = 0

class InventoryTransactionCreate(BaseModel):
    transaction_type: str
    quantity: float
    remarks: str | None = None

class InventoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    expedition_id: int
    item_name: str
    category: str
    quantity: float
    unit: str
    min_quantity: float
    status: str
