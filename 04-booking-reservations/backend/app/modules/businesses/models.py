from app.core.common import Repository


def unsplash(photo_id: str) -> str:
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop"


CATEGORIES = [
    {"slug": "clinics", "name": "Clinics & dentists", "icon": "Stethoscope"},
    {"slug": "restaurants", "name": "Restaurants", "icon": "Utensils"},
    {"slug": "salons", "name": "Salons & barbers", "icon": "Scissors"},
    {"slug": "repair", "name": "Repair shops", "icon": "Wrench"},
    {"slug": "training", "name": "Training & consultants", "icon": "GraduationCap"},
]


def _svc(i, name, minutes, price, deposit=0, per_person=False):
    return {"id": i, "name": name, "minutes": minutes, "price": price, "deposit": deposit, "per_person": per_person}


def _staff(i, name, role, max_party=None):
    return {"id": i, "name": name, "role": role, "max_party": max_party}


# kind: "appointment" → pick a staff member; "table" → pick party size, staff = seating areas
businesses = Repository([
    {"slug": "brightsmile-dental", "name": "BrightSmile Dental", "category": "clinics", "kind": "appointment", "image": unsplash("1629909613654-28e377c37b09"),
     "area": "Marylebone, London", "rating": 4.9, "reviews": 412, "open": "08:00", "close": "18:00", "slot_minutes": 15,
     "about": "Modern family dentistry with same-week appointments, digital X-rays and a calm, anxiety-friendly team.",
     "services": [_svc(1, "Check-up & hygiene clean", 45, 80), _svc(2, "Teeth whitening", 60, 250, deposit=50), _svc(3, "Composite filling", 45, 140), _svc(4, "Emergency visit", 30, 95)],
     "staff": [_staff(1, "Dr. Elena Varga", "Dentist"), _staff(2, "Dr. Sam Okafor", "Dentist"), _staff(3, "Lucy Hart", "Hygienist")]},
    {"slug": "citycare-clinic", "name": "CityCare Family Clinic", "category": "clinics", "kind": "appointment", "image": unsplash("1519494026892-80bbd2d6fd0d"),
     "area": "Shoreditch, London", "rating": 4.7, "reviews": 238, "open": "08:30", "close": "19:00", "slot_minutes": 15,
     "about": "GP consultations, blood tests, vaccinations and physiotherapy under one roof — booked online in seconds.",
     "services": [_svc(1, "GP consultation", 20, 60), _svc(2, "Blood test", 15, 35), _svc(3, "Travel vaccination", 15, 40), _svc(4, "Physiotherapy session", 45, 75)],
     "staff": [_staff(1, "Dr. Mira Patel", "General practitioner"), _staff(2, "Dr. Jonas Berg", "General practitioner"), _staff(3, "Ana Lopez", "Physiotherapist")]},
    {"slug": "olive-and-ember", "name": "Olive & Ember", "category": "restaurants", "kind": "table", "image": unsplash("1517248135467-4c7edcad34c4"),
     "area": "Covent Garden, London", "rating": 4.8, "reviews": 1290, "open": "12:00", "close": "22:00", "slot_minutes": 30,
     "about": "Wood-fired Mediterranean plates, natural wines and a lively open kitchen.",
     "services": [_svc(1, "Lunch table", 75, 0), _svc(2, "Dinner table", 105, 0), _svc(3, "Chef's tasting menu", 150, 85, deposit=20, per_person=True)],
     "staff": [_staff(1, "Main room", "Up to 6 guests", 6), _staff(2, "Terrace", "Up to 4 guests", 4), _staff(3, "Private room", "Up to 12 guests", 12)]},
    {"slug": "maison-lumiere", "name": "Maison Lumière", "category": "restaurants", "kind": "table", "image": unsplash("1414235077428-338989a2e8c0"),
     "area": "Mayfair, London", "rating": 4.9, "reviews": 684, "open": "18:00", "close": "23:00", "slot_minutes": 30,
     "about": "Modern French fine dining with a seasonal seven-course menu.",
     "services": [_svc(1, "À la carte dinner", 120, 0), _svc(2, "Seven-course tasting", 180, 145, deposit=50, per_person=True)],
     "staff": [_staff(1, "Dining room", "Up to 6 guests", 6), _staff(2, "Chef's counter", "Up to 2 guests", 2)]},
    {"slug": "studio-rouge", "name": "Studio Rouge Salon", "category": "salons", "kind": "appointment", "image": unsplash("1521590832167-7bcbfaa6381f"),
     "area": "Notting Hill, London", "rating": 4.8, "reviews": 527, "open": "09:00", "close": "20:00", "slot_minutes": 15,
     "about": "Precision cuts, lived-in colour and nail care by an award-winning team.",
     "services": [_svc(1, "Cut & finish", 45, 55), _svc(2, "Full colour", 120, 140, deposit=30), _svc(3, "Blow-dry", 30, 35), _svc(4, "Gel manicure", 40, 30)],
     "staff": [_staff(1, "Chloe Dubois", "Senior stylist"), _staff(2, "Marco Rinaldi", "Colourist"), _staff(3, "Aisha Khan", "Nail technician")]},
    {"slug": "gentlemans-chair", "name": "The Gentleman's Chair", "category": "salons", "kind": "appointment", "image": unsplash("1600948836101-f9ffda59d250"),
     "area": "Soho, London", "rating": 4.6, "reviews": 311, "open": "10:00", "close": "19:00", "slot_minutes": 15,
     "about": "Classic barbering, hot-towel shaves and beard sculpting.",
     "services": [_svc(1, "Classic cut", 30, 28), _svc(2, "Beard trim & shape", 20, 18), _svc(3, "Hot-towel shave", 30, 32)],
     "staff": [_staff(1, "Leo Grant", "Barber"), _staff(2, "Tariq Aziz", "Barber")]},
    {"slug": "fixpoint-repair", "name": "FixPoint Auto & Phone Repair", "category": "repair", "kind": "appointment", "image": unsplash("1486262715619-67b85e0b08d3"),
     "area": "Camden, London", "rating": 4.5, "reviews": 196, "open": "08:00", "close": "17:30", "slot_minutes": 30,
     "about": "Fixed-price car servicing, diagnostics and same-day phone screen repairs.",
     "services": [_svc(1, "Car diagnostics", 60, 70), _svc(2, "Oil & filter service", 60, 90), _svc(3, "Phone screen repair", 60, 120, deposit=20), _svc(4, "Laptop health check", 30, 40)],
     "staff": [_staff(1, "Bay 1 · Dan", "Mechanic"), _staff(2, "Bay 2 · Raj", "Mechanic"), _staff(3, "Tech desk · Mei", "Device technician")]},
    {"slug": "northstar-training", "name": "Northstar Training Centre", "category": "training", "kind": "appointment", "image": unsplash("1524178232363-1fb2b075b655"),
     "area": "King's Cross, London", "rating": 4.7, "reviews": 158, "open": "09:00", "close": "18:00", "slot_minutes": 30,
     "about": "Hands-on workshops in Excel, data and leadership plus 1:1 career coaching.",
     "services": [_svc(1, "Course advice call", 30, 0), _svc(2, "Excel masterclass (1:1)", 120, 160), _svc(3, "Career coaching", 60, 90)],
     "staff": [_staff(1, "Hannah Reid", "Data trainer"), _staff(2, "Victor Osei", "Career coach")]},
    {"slug": "apex-advisory", "name": "Apex Advisory", "category": "training", "kind": "appointment", "image": unsplash("1600880292203-757bb62b4baf"),
     "area": "City of London", "rating": 4.9, "reviews": 87, "open": "09:00", "close": "17:00", "slot_minutes": 30,
     "about": "Independent consultants for strategy, tax and funding — book a focused session.",
     "services": [_svc(1, "Free intro call", 15, 0), _svc(2, "Strategy session", 60, 250, deposit=50), _svc(3, "Tax consultation", 45, 150)],
     "staff": [_staff(1, "Grace Liu", "Strategy partner"), _staff(2, "Omar Haddad", "Tax advisor")]},
], key="slug")
