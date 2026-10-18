from typing import Literal

from pydantic import BaseModel

from app.core.common import Repository


class ReportIn(BaseModel):
    template_id: str
    period: Literal["7d", "30d", "90d"] = "30d"


class ScheduleIn(BaseModel):
    template_id: str
    frequency: Literal["daily", "weekly", "monthly"]
    channel: Literal["email", "whatsapp", "slack"]
    recipient: str


TEMPLATES = [
    {"id": "sales", "name": "Sales performance", "description": "Revenue, orders, AOV and top products", "icon": "TrendingUp",
     "kpis": [("Revenue", "$", 182000), ("Orders", "", 2140), ("Avg. order value", "$", 85), ("Conversion", "%", 3.2)],
     "breakdown": ["Online store", "Marketplace", "Wholesale", "Retail"]},
    {"id": "support", "name": "Support operations", "description": "Tickets, AI resolution rate and CSAT", "icon": "Headphones",
     "kpis": [("Tickets", "", 3480), ("AI resolved", "%", 71), ("First response", "s", 1.4), ("CSAT", "/5", 4.6)],
     "breakdown": ["Order status", "Returns", "Product info", "Billing"]},
    {"id": "finance", "name": "Finance summary", "description": "Cash in, cash out, receivables and margin", "icon": "Landmark",
     "kpis": [("Cash in", "$", 241000), ("Cash out", "$", 176000), ("Receivables", "$", 58200), ("Gross margin", "%", 41)],
     "breakdown": ["Payroll", "Suppliers", "Marketing", "Software"]},
]
schedules = Repository([
    {"id": 1, "template_id": "sales", "frequency": "weekly", "channel": "email", "recipient": "leadership@lumenhome.com", "next_run": "Monday 08:00"},
    {"id": 2, "template_id": "support", "frequency": "daily", "channel": "slack", "recipient": "#support-ops", "next_run": "Tomorrow 09:00"},
    {"id": 3, "template_id": "finance", "frequency": "monthly", "channel": "whatsapp", "recipient": "+44 7700 900123", "next_run": "Nov 1, 08:00"},
])
