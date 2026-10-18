from datetime import date

from app.core.common import TODAY, days
from app.modules.fleet.models import ServiceIn, logs, vehicles


def present(v: dict) -> dict:
    expiry_days = (date.fromisoformat(v["insurance_expiry"]) - TODAY).days
    km_left = v["next_service_km"] - v["mileage"]
    return {**v, "km_to_service": km_left, "insurance_days_left": expiry_days,
            "service_due": km_left <= 500, "insurance_alert": expiry_days <= 30}


def list_vehicles() -> list[dict]:
    return [present(v) for v in vehicles.all()]


def alerts() -> list[dict]:
    out = []
    for v in list_vehicles():
        if v["service_due"]:
            out.append({"type": "service", "message": f"{v['plate']} {v['model']} is due for service"})
        if v["insurance_alert"]:
            out.append({"type": "insurance",
                        "message": f"{v['plate']} insurance expires in {v['insurance_days_left']} days"})
    return out


def log_service(vehicle_id: int, data: ServiceIn) -> dict:
    v = vehicles.get_or_404(vehicle_id)
    v.update(last_service=days(0), next_service_km=v["mileage"] + 10000, status="active")
    logs.add({"id": len(logs.rows) + 1, "vehicle_id": v["id"], "plate": v["plate"], "date": days(0),
              "notes": data.notes, "cost": data.cost})
    return present(v)


def renew_insurance(vehicle_id: int) -> dict:
    v = vehicles.get_or_404(vehicle_id)
    v["insurance_expiry"] = days(365)
    return present(v)
