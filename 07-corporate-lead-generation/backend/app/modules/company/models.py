from pydantic import BaseModel, Field

from app.core.common import Repository, days


def unsplash(photo_id: str) -> str:
    return f"https://images.unsplash.com/photo-{photo_id}?auto=format&fit=crop"


class ContactIn(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    company: str = ""
    phone: str = ""
    topic: str = "General enquiry"
    message: str = Field(min_length=5)


COMPANY = {
    "name": "Vertex Industrial", "founded": 1987, "hq": "Birmingham, United Kingdom",
    "stats": [{"value": "38", "label": "years engineering"}, {"value": "1,450", "label": "employees"}, {"value": "62", "label": "countries served"}, {"value": "ISO 9001", "label": "& 14001 certified"}],
    "hero_image": unsplash("1513828583688-c52646db42da"),
}

SERVICES = [
    {"slug": "precision-manufacturing", "title": "Precision manufacturing", "icon": "Cog", "image": unsplash("1581091226825-a6a2a5aee158"),
     "summary": "CNC machining, fabrication and assembly to ±0.005 mm tolerances, from prototype to high-volume runs.",
     "points": ["5-axis CNC machining", "Sheet-metal fabrication", "Robotic welding", "Clean-room assembly"]},
    {"slug": "engineering-design", "title": "Engineering & design", "icon": "PenTool", "image": unsplash("1581092160562-40aa08e78837"),
     "summary": "Mechanical and electrical engineering teams that design for manufacturability, cost and compliance.",
     "points": ["CAD/CAE & simulation", "DFM reviews", "CE/UKCA certification support", "Reverse engineering"]},
    {"slug": "installation-maintenance", "title": "Installation & maintenance", "icon": "Wrench", "image": unsplash("1504307651254-35680f356dfd"),
     "summary": "Nationwide field engineers for installation, commissioning and planned preventive maintenance.",
     "points": ["24/7 emergency call-out", "Predictive maintenance (IoT)", "Spare-parts logistics", "Operator training"]},
    {"slug": "automation-controls", "title": "Automation & controls", "icon": "Cpu", "image": unsplash("1565043666747-69f6646db940"),
     "summary": "PLC, SCADA and robotics integration that lifts throughput and cuts downtime.",
     "points": ["PLC & SCADA programming", "Robotic cells", "Machine vision QA", "OEE dashboards"]},
]

INDUSTRIES = ["Automotive", "Food & beverage", "Pharmaceutical", "Energy & utilities", "Water treatment", "Aerospace"]

CASE_STUDIES = [
    {"client": "Northline Foods", "industry": "Food & beverage", "result": "+31% line throughput", "summary": "Automated a bottling line with vision QA and hygienic pumps, paying back in 14 months."},
    {"client": "Aquaterra Water", "industry": "Water treatment", "result": "-42% energy use", "summary": "Replaced 120 legacy pumps with VSD-driven units and remote monitoring across 18 sites."},
    {"client": "Kestrel Automotive", "industry": "Automotive", "result": "0.2% scrap rate", "summary": "Designed and built 6 robotic welding cells with in-line metrology for a new EV platform."},
]

messages = Repository([
    {"id": 1, "name": "Laura Mills", "email": "laura@greenfield.co.uk", "company": "Greenfield Dairy", "phone": "", "topic": "Maintenance contract",
     "message": "We need a PPM contract for 3 sites in Yorkshire.", "created": days(-1), "status": "new"},
])
