"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.contact.controller import router as contact
from app.modules.profile.controller import router as profile
from app.modules.projects.controller import router as projects

ROUTERS = [profile, projects, contact]
