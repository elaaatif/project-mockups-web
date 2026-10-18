from pydantic import BaseModel, Field

from app.core.common import Repository, days, rng


class ServiceIn(BaseModel):
    notes: str = Field(min_length=2)
    cost: float = Field(ge=0)


_VEHICLES = [("Ford Transit", "Van"), ("Mercedes Sprinter", "Van"), ("Volvo FH16", "Truck"),
             ("Isuzu NPR", "Truck"), ("Toyota Hilux", "Pickup"), ("Toyota Corolla", "Car"),
             ("Renault Master", "Van"), ("MAN TGS", "Truck"), ("Nissan Navara", "Pickup")]
_DRIVERS = ["Ethan Clarke", "Yusuf Demir", "Noah Becker", "Marco Silva", "Ali Rahman", "Jonas Weber",
            "Kenji Ito", "Pierre Dubois", "Sam Osei"]


def _seed(i: int, model: str, kind: str) -> dict:
    mileage = rng.randint(18000, 190000)
    return {
        "id": i + 1, "plate": f"{rng.choice('ABCDKM')}{rng.choice('ABTXZ')}-{rng.randint(1000, 9999)}",
        "model": model, "type": kind, "driver": _DRIVERS[i], "mileage": mileage,
        "next_service_km": mileage + rng.randint(-800, 9000), "last_service": days(-rng.randint(20, 200)),
        "insurance_provider": rng.choice(["AXA", "Allianz", "Zurich", "Chubb"]),
        "insurance_expiry": days(rng.randint(-5, 300)), "fuel_efficiency": round(rng.uniform(6, 28), 1),
        "status": rng.choice(["active", "active", "active", "idle"]),
    }


vehicles = Repository([_seed(i, m, k) for i, (m, k) in enumerate(_VEHICLES)])
logs = Repository([
    {"id": i + 1, "vehicle_id": v["id"], "plate": v["plate"], "date": days(-rng.randint(5, 120)),
     "notes": rng.choice(["Oil & filter change", "Tyre rotation", "Brake inspection", "Annual inspection"]),
     "cost": round(rng.uniform(90, 1400), 2)}
    for i, v in enumerate(rng.sample(vehicles.all(), 6))
])
