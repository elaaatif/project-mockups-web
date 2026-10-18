"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.agent.controller import router as agent
from app.modules.leads.controller import router as leads
from app.modules.listings.controller import router as listings
from app.modules.plans.controller import router as plans
from app.modules.rentals.controller import router as rentals

ROUTERS = [listings, leads, agent, rentals, plans]
