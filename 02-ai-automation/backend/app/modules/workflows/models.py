from pydantic import BaseModel, Field

from app.core.common import Repository


class Step(BaseModel):
    type: str
    label: str


class WorkflowIn(BaseModel):
    name: str = Field(min_length=3)
    trigger: Step
    steps: list[Step] = Field(min_length=1)


# Building blocks shown in the visual builder
CATALOG = {
    "triggers": [
        {"type": "email_received", "label": "Email received", "channel": "email"},
        {"type": "whatsapp_message", "label": "WhatsApp message", "channel": "whatsapp"},
        {"type": "form_submitted", "label": "Website form submitted", "channel": "web"},
        {"type": "schedule", "label": "On a schedule", "channel": "time"},
        {"type": "new_order", "label": "New Shopify order", "channel": "web"},
    ],
    "actions": [
        {"type": "ai_classify", "label": "AI: classify intent"},
        {"type": "ai_extract", "label": "AI: extract data from attachment"},
        {"type": "ai_reply", "label": "AI: draft reply"},
        {"type": "ai_summarize", "label": "AI: summarize"},
        {"type": "send_whatsapp", "label": "Send WhatsApp message"},
        {"type": "send_email", "label": "Send email"},
        {"type": "crm_update", "label": "Create / update CRM record"},
        {"type": "sheet_append", "label": "Append row to Google Sheet"},
        {"type": "erp_post", "label": "Post to ERP (HTTP)"},
        {"type": "condition", "label": "If / else condition"},
        {"type": "notify_slack", "label": "Notify Slack channel"},
    ],
}

workflows = Repository([
    {"id": 1, "name": "Supplier invoices → ERP", "enabled": True, "runs": 1284, "success_rate": 98.7, "last_run": "3 min ago",
     "trigger": {"type": "email_received", "label": "Email received at invoices@"},
     "steps": [{"type": "ai_extract", "label": "AI: extract invoice fields"}, {"type": "condition", "label": "If total > $5,000"},
               {"type": "notify_slack", "label": "Ask finance to approve"}, {"type": "erp_post", "label": "Post bill to ERP"}]},
    {"id": 2, "name": "WhatsApp lead qualifier", "enabled": True, "runs": 642, "success_rate": 96.1, "last_run": "11 min ago",
     "trigger": {"type": "whatsapp_message", "label": "New WhatsApp message"},
     "steps": [{"type": "ai_classify", "label": "AI: classify intent & budget"}, {"type": "crm_update", "label": "Create lead in HubSpot"},
               {"type": "send_whatsapp", "label": "Send booking link"}]},
    {"id": 3, "name": "Weekly KPI digest", "enabled": True, "runs": 41, "success_rate": 100.0, "last_run": "Mon 08:00",
     "trigger": {"type": "schedule", "label": "Every Monday 08:00"},
     "steps": [{"type": "ai_summarize", "label": "AI: summarize weekly metrics"}, {"type": "send_email", "label": "Email leadership team"}]},
    {"id": 4, "name": "Support email triage", "enabled": False, "runs": 2210, "success_rate": 93.4, "last_run": "2 days ago",
     "trigger": {"type": "email_received", "label": "Email received at support@"},
     "steps": [{"type": "ai_classify", "label": "AI: classify & prioritise"}, {"type": "ai_reply", "label": "AI: draft reply"},
               {"type": "condition", "label": "If confidence > 90%"}, {"type": "send_email", "label": "Send reply"}]},
    {"id": 5, "name": "Order confirmation via WhatsApp", "enabled": True, "runs": 3920, "success_rate": 99.5, "last_run": "just now",
     "trigger": {"type": "new_order", "label": "New Shopify order"},
     "steps": [{"type": "send_whatsapp", "label": "Send order confirmation"}, {"type": "sheet_append", "label": "Log to fulfilment sheet"}]},
])
