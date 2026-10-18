from fastapi import APIRouter

from app.modules.profile.models import PACKAGES, PROFILE, RETAINERS, SKILLS, TESTIMONIALS

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("")
def profile():
    return PROFILE | {"skills": SKILLS, "packages": PACKAGES, "retainers": RETAINERS, "testimonials": TESTIMONIALS}
