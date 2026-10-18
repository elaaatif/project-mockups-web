import re

from app.core.common import Repository, rng


def unsplash(photo_id: str) -> str:
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop"


EXTERIORS = ["1512917774080-9991f1c4c750", "1564013799919-ab600027ffc6", "1568605114967-8130f3a36994", "1570129477492-45c003edd2be",
             "1580587771525-78b9dba3b914", "1600585154340-be6161a56a0c", "1600596542815-ffad4c1539a9", "1613490493576-7fde63acd811"]
INTERIORS = ["1493809842364-78817add7ffb", "1502672260266-1c1ef2d93688", "1505693416388-ac5ce068fe85", "1522708323590-d24dbb6b0267",
             "1524758631624-e2822e304c36", "1560448204-e02f11c3d0e2", "1484154218962-a197022b5858", "1586023492125-27b2c045efd7"]

agents = Repository([
    {"id": 1, "name": "Sophie Bennett", "title": "Senior Sales Agent", "phone": "+44 20 7946 0101", "email": "sophie@haven.estate", "photo": unsplash("1494790108377-be9c29b29330"), "deals": 64},
    {"id": 2, "name": "James Okoro", "title": "Lettings Manager", "phone": "+44 20 7946 0102", "email": "james@haven.estate", "photo": unsplash("1507003211169-0a1dd7228f2d"), "deals": 112},
    {"id": 3, "name": "Clara Novak", "title": "Prime Property Specialist", "phone": "+44 20 7946 0103", "email": "clara@haven.estate", "photo": unsplash("1438761681033-6461ffad8d80"), "deals": 41},
    {"id": 4, "name": "Daniel Reyes", "title": "Sales Agent", "phone": "+44 20 7946 0104", "email": "daniel@haven.estate", "photo": unsplash("1500648767791-00dcc994a43e"), "deals": 38},
])

DISTRICTS = {  # avg £/sqm used for valuations, plus map centre
    "Chelsea": (16500, 51.4875, -0.1687), "Hampstead": (12800, 51.5557, -0.1780), "Islington": (10900, 51.5362, -0.1033),
    "Canary Wharf": (11200, 51.5054, -0.0235), "Richmond": (9800, 51.4613, -0.3037), "Clapham": (9400, 51.4621, -0.1380),
    "Notting Hill": (15200, 51.5096, -0.1967), "Greenwich": (8200, 51.4826, -0.0077),
}

_SEED = [
    ("Contemporary villa with pool", "villa", "sale", 4_250_000, 5, 5, 420, "Richmond", True),
    ("Garden-square family house", "house", "sale", 2_950_000, 4, 3, 245, "Chelsea", True),
    ("Light-filled penthouse with terrace", "penthouse", "sale", 1_875_000, 3, 2, 148, "Canary Wharf", True),
    ("Victorian terrace, fully restored", "house", "sale", 1_350_000, 4, 2, 165, "Clapham", False),
    ("Two-bed apartment by the canal", "apartment", "sale", 785_000, 2, 2, 84, "Islington", False),
    ("Heath-side Edwardian home", "house", "sale", 3_400_000, 5, 4, 310, "Hampstead", False),
    ("Riverside studio with concierge", "apartment", "rent", 2_150, 1, 1, 42, "Greenwich", False),
    ("Designer two-bed with balcony", "apartment", "rent", 3_400, 2, 2, 78, "Notting Hill", True),
    ("Family townhouse near the park", "house", "rent", 5_900, 4, 3, 190, "Richmond", False),
    ("Loft apartment in converted warehouse", "apartment", "rent", 2_950, 2, 1, 88, "Islington", False),
    ("Modern villa with home cinema", "villa", "sale", 5_600_000, 6, 6, 520, "Hampstead", False),
    ("Sky-high one-bed with gym & pool", "apartment", "rent", 2_600, 1, 1, 55, "Canary Wharf", False),
]
FEATURES = ["Garden", "Parking", "Balcony", "Concierge", "Gym", "Pool", "EV charging", "Home office", "Air conditioning", "Lift", "Pet friendly", "Fibre broadband"]


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


properties = Repository([
    {
        "id": i + 1, "slug": _slug(title), "title": title, "type": kind, "purpose": purpose, "price": price, "beds": beds,
        "baths": baths, "area_sqm": area, "district": district, "address": f"{rng.randint(2, 98)} {rng.choice(['Elm', 'Kings', 'Park', 'Mill', 'Rose', 'Queens'])} {rng.choice(['Road', 'Gardens', 'Lane', 'Terrace'])}, {district}",
        "lat": DISTRICTS[district][1] + rng.uniform(-0.008, 0.008), "lng": DISTRICTS[district][2] + rng.uniform(-0.012, 0.012),
        "images": [unsplash(EXTERIORS[i % len(EXTERIORS)] if kind != "apartment" else INTERIORS[i % len(INTERIORS)])] + [unsplash(x) for x in rng.sample(INTERIORS, 4)],
        "features": rng.sample(FEATURES, 5), "agent_id": 2 if purpose == "rent" else rng.choice([1, 3, 4]),
        "status": "under_offer" if i in (3, 10) else "available", "featured": featured, "year_built": rng.choice([1890, 1910, 1965, 2008, 2019, 2023]),
        "energy": rng.choice(["A", "B", "B", "C", "D"]), "listed_days": rng.randint(1, 60), "views": rng.randint(120, 4200),
        "description": f"A beautifully presented {kind} in the heart of {district}, offering {area} m² of living space across generous, light-filled rooms. "
                       "Highlights include a bespoke kitchen, high ceilings, quality finishes throughout and excellent transport links.",
    }
    for i, (title, kind, purpose, price, beds, baths, area, district, featured) in enumerate(_SEED)
], key="slug")
