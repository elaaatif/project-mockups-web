"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.bookings.controller import router as bookings
from app.modules.businesses.controller import router as businesses
from app.modules.dashboard.controller import router as dashboard
from app.modules.plans.controller import router as plans

ROUTERS = [businesses, bookings, dashboard, plans]
