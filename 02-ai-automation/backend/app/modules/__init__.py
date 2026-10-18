"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.chatbot.controller import router as chatbot
from app.modules.extraction.controller import router as extraction
from app.modules.overview.controller import router as overview
from app.modules.pricing.controller import router as pricing
from app.modules.reports.controller import router as reports
from app.modules.workflows.controller import router as workflows

ROUTERS = [overview, chatbot, extraction, reports, workflows, pricing]
