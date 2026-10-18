from app.core.common import Repository, days, rng

jobs = Repository([
    {"id": 1, "slug": "senior-mechanical-design-engineer", "title": "Senior Mechanical Design Engineer", "department": "Engineering", "location": "Birmingham", "type": "Full-time", "remote": "Hybrid", "salary": "£55k–£68k", "posted": days(-3),
     "summary": "Lead the design of pump and valve assemblies from concept to production.",
     "responsibilities": ["Own 3D CAD design and FEA for new products", "Run DFM reviews with manufacturing", "Mentor two graduate engineers"],
     "requirements": ["Degree in mechanical engineering", "5+ years in product design", "SolidWorks or Creo expertise"]},
    {"id": 2, "slug": "field-service-engineer-north", "title": "Field Service Engineer (North)", "department": "Service", "location": "Leeds", "type": "Full-time", "remote": "On-site", "salary": "£38k–£46k + van", "posted": days(-6),
     "summary": "Install, commission and maintain equipment at customer sites across the North of England.",
     "responsibilities": ["Commission pumps, VSDs and compressors", "Planned and reactive maintenance", "Customer training on site"],
     "requirements": ["Electrical or mechanical NVQ Level 3", "Full UK driving licence", "18th Edition preferred"]},
    {"id": 3, "slug": "plc-automation-engineer", "title": "PLC & Automation Engineer", "department": "Automation", "location": "Birmingham", "type": "Full-time", "remote": "Hybrid", "salary": "£48k–£60k", "posted": days(-1),
     "summary": "Program and integrate PLC, SCADA and robotic systems for customer lines.",
     "responsibilities": ["Write IEC 61131-3 code", "Integrate robots & vision systems", "Support FAT/SAT"],
     "requirements": ["Siemens or Rockwell experience", "3+ years in automation", "Willing to travel 30%"]},
    {"id": 4, "slug": "cnc-machinist-nights", "title": "CNC Machinist (Nights)", "department": "Manufacturing", "location": "Coventry", "type": "Full-time", "remote": "On-site", "salary": "£34k–£39k", "posted": days(-10),
     "summary": "Set and operate 5-axis CNC machines producing precision components.",
     "responsibilities": ["Set up and prove programs", "In-process inspection", "Continuous improvement"],
     "requirements": ["Experience with Mazak or DMG Mori", "Read engineering drawings", "Night-shift availability"]},
    {"id": 5, "slug": "technical-sales-manager-dach", "title": "Technical Sales Manager — DACH", "department": "Sales", "location": "Munich", "type": "Full-time", "remote": "Remote", "salary": "€85k–€100k + bonus", "posted": days(-4),
     "summary": "Grow our pumps and automation business across Germany, Austria and Switzerland.",
     "responsibilities": ["Own the regional pipeline", "Lead technical presentations", "Work with distributors"],
     "requirements": ["Fluent German and English", "B2B industrial sales track record", "Engineering background"]},
    {"id": 6, "slug": "graduate-engineer-2027", "title": "Graduate Engineer Programme 2027", "department": "Engineering", "location": "Birmingham", "type": "Graduate", "remote": "On-site", "salary": "£32k", "posted": days(-14),
     "summary": "A two-year rotational programme across design, manufacturing and field service.",
     "responsibilities": ["Four 6-month rotations", "Chartership support (IMechE/IET)", "Real projects from day one"],
     "requirements": ["2:1 in an engineering discipline", "Graduating in 2026 or 2027", "Right to work in the UK"]},
], key="slug")

applications = Repository([
    {"id": i + 1, "job_id": j, "job_title": next(x["title"] for x in jobs.all() if x["id"] == j), "name": n, "email": n.split()[0].lower() + "@mail.com",
     "phone": "", "linkedin": "", "cover": "", "cv_name": f"{n.split()[0]}_CV.pdf", "status": s, "created": days(-rng.randint(0, 12)), "rating": rng.randint(2, 5)}
    for i, (j, n, s) in enumerate([(1, "Olivia Hart", "interviewing"), (1, "Kwame Mensah", "new"), (2, "Ryan Doyle", "new"), (3, "Lena Vogel", "interviewing"),
                                   (3, "Arash Karimi", "rejected"), (5, "Jonas Fischer", "new"), (6, "Grace Obi", "new"), (6, "Ben Walsh", "hired")])
])
