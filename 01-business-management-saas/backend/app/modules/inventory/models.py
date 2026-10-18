from pydantic import BaseModel, Field

from app.core.common import Repository, rng


class ItemIn(BaseModel):
    name: str = Field(min_length=2)
    category: str
    qty: int = Field(ge=0)
    reorder_level: int = Field(ge=0)
    unit_cost: float = Field(gt=0)
    location: str = "Warehouse A"
    supplier: str = "Unassigned"


class StockAdjust(BaseModel):
    delta: int
    reason: str = "Manual adjustment"


CATEGORIES = ["Raw Materials", "Packaging", "Electronics", "Office", "Spare Parts"]
_SEED = [
    ("Steel Sheet 2mm", "Raw Materials", "Metalco Supply"), ("Aluminium Rod 12mm", "Raw Materials", "Metalco Supply"),
    ("Corrugated Box L", "Packaging", "PackRight"), ("Bubble Wrap Roll", "Packaging", "PackRight"),
    ("Pallet Stretch Film", "Packaging", "PackRight"), ("Barcode Scanner X2", "Electronics", "TechSource"),
    ("Thermal Label Printer", "Electronics", "TechSource"), ("Li-ion Battery Pack", "Electronics", "VoltCore"),
    ("A4 Copy Paper (box)", "Office", "OfficeHub"), ("Toner Cartridge 85A", "Office", "OfficeHub"),
    ("Hydraulic Filter", "Spare Parts", "FleetParts Co"), ("Brake Pad Set", "Spare Parts", "FleetParts Co"),
    ("V-Belt B48", "Spare Parts", "FleetParts Co"), ("Copper Wire 2.5mm", "Raw Materials", "Metalco Supply"),
]
items = Repository([
    {
        "sku": f"SKU-{1001 + i}", "name": n, "category": c, "supplier": s,
        "qty": rng.randint(0, 35) if i % 4 == 1 else rng.randint(60, 420), "reorder_level": rng.choice([20, 40, 60]),
        "unit_cost": round(rng.uniform(2, 260), 2),
        "location": rng.choice(["Warehouse A", "Warehouse B", "Store Room"]),
    }
    for i, (n, c, s) in enumerate(_SEED)
], key="sku")
