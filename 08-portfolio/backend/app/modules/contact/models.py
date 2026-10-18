from typing import Literal

from pydantic import BaseModel, Field

from app.core.common import Repository

PROJECT_TYPES = {  # base price, base weeks
    "corporate": ("Corporate / lead-gen website", 1500, 2),
    "ecommerce": ("E-commerce store", 5500, 5),
    "booking": ("Booking & reservations", 6000, 6),
    "real_estate": ("Real estate platform", 7500, 7),
    "education": ("Education / LMS", 7000, 7),
    "saas": ("Business management SaaS", 12000, 10),
    "ai": ("AI automation", 6500, 5),
}
ADDONS = {  # price, weeks
    "payments": ("Online payments", 900, 1), "multilingual": ("Multi-language", 1200, 1), "mobile_app": ("Mobile app (PWA)", 3500, 3),
    "ai_chatbot": ("AI chatbot", 2500, 2), "integrations": ("ERP / CRM integration", 2000, 2), "seo": ("SEO & content setup", 800, 1),
}


class EstimateIn(BaseModel):
    project_type: str
    addons: list[str] = []
    urgency: Literal["standard", "fast"] = "standard"


class MessageIn(BaseModel):
    name: str = Field(min_length=2)
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    company: str = ""
    project_type: str = ""
    budget: str = ""
    message: str = Field(min_length=10)
    estimate: dict | None = None


class StatusIn(BaseModel):
    status: Literal["new", "contacted", "won", "closed"]


messages = Repository([])
