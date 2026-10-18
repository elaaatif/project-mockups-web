"""Module registry. To add a feature: create app/modules/<name>/{models,service,controller}.py
and append its router here."""
from app.modules.academy.controller import router as academy
from app.modules.courses.controller import router as courses
from app.modules.learning.controller import router as learning
from app.modules.plans.controller import router as plans
from app.modules.training.controller import router as training

ROUTERS = [courses, learning, training, academy, plans]
