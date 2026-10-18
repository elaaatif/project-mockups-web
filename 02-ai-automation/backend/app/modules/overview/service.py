"""Overview aggregates other modules — it owns no data."""
from app.core.common import rng
from app.modules.chatbot import service as chatbot
from app.modules.workflows.models import workflows

_DAILY = [round(380 + i * 9 + rng.uniform(-60, 80)) for i in range(30)]


def overview() -> dict:
    runs = sum(w["runs"] for w in workflows.all())
    return {
        "kpis": {"hours_saved": round(runs * 4 / 60), "tasks_automated": runs, "ai_resolution": chatbot.inbox()["stats"]["ai_resolution"],
                 "documents_processed": 1284, "active_workflows": sum(w["enabled"] for w in workflows.all())},
        "daily": {"labels": [f"{i + 1}" for i in range(30)], "values": _DAILY},
        "channels": {"labels": ["Email", "WhatsApp", "Web chat", "Scheduled"], "values": [42, 31, 19, 8]},
        "savings": {"manual_cost": round(runs * 4 / 60 * 32), "platform_cost": 799},
    }
