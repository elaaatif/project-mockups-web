from app.modules.billing.models import ANNUAL_DISCOUNT, PLANS, SUPPORT_CONTRACTS


def catalog() -> dict:
    plans = [{**p, "annual": round(p["monthly"] * (1 - ANNUAL_DISCOUNT))} for p in PLANS]
    return {"plans": plans, "support": SUPPORT_CONTRACTS, "annual_discount": ANNUAL_DISCOUNT}
