from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng
from app.modules.catalog.models import products


class CustomerIn(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    address: str = Field(min_length=3)
    city: str
    country: str = "United Kingdom"


class LineIn(BaseModel):
    product_id: int
    qty: int = Field(gt=0, le=999)


class OrderIn(BaseModel):
    customer: CustomerIn
    items: list[LineIn] = Field(min_length=1)
    shipping: Literal["standard", "express"] = "standard"
    payment: Literal["card", "paypal", "cod"] = "card"


STAGES = ["placed", "paid", "packed", "shipped", "out_for_delivery", "delivered"]
STAGE_LABELS = {"placed": "Order placed", "paid": "Payment confirmed", "packed": "Packed at warehouse",
                "shipped": "Handed to carrier", "out_for_delivery": "Out for delivery", "delivered": "Delivered"}
SHIPPING = {"standard": 4.9, "express": 12.9}
FREE_SHIPPING_OVER = 75
TAX_RATE = 0.2

_NAMES = [("Olivia Brown", "olivia@example.com"), ("Liam Chen", "liam@example.com"), ("Sofia Garcia", "sofia@example.com"),
          ("Noah Smith", "noah@example.com"), ("Ava Johnson", "ava@example.com"), ("Mateo Rossi", "mateo@example.com"),
          ("Hannah Weber", "hannah@example.com"), ("Yusuf Kaya", "yusuf@example.com")]


def _seed(i: int, name: str, email: str) -> dict:
    picks = rng.sample(products.all(), rng.randint(1, 3))
    items = [{"product_id": p["id"], "name": p["name"], "image": p["image"], "qty": rng.randint(1, 2), "unit_price": p["price"]} for p in picks]
    subtotal = sum(x["qty"] * x["unit_price"] for x in items)
    stage = i % len(STAGES)
    return {
        "id": f"MC-{48210 + i}", "channel": "retail", "customer": {"name": name, "email": email, "address": "12 King St", "city": "London", "country": "United Kingdom"},
        "items": items, "subtotal": subtotal, "shipping_cost": 0 if subtotal > FREE_SHIPPING_OVER else 4.9,
        "tax": round(subtotal * TAX_RATE / (1 + TAX_RATE), 2), "total": subtotal + (0 if subtotal > FREE_SHIPPING_OVER else 4.9),
        "shipping": "standard", "payment": "card", "stage": stage, "created": days(-(len(STAGES) - stage)),
        "history": [days(-(len(STAGES) - s)) for s in range(stage + 1)], "carrier": "DHL Express", "tracking_no": f"JD0146{rng.randint(10000000, 99999999)}",
    }


orders = Repository([_seed(i, n, e) for i, (n, e) in enumerate(_NAMES)])
