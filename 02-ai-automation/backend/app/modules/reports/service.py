"""Builds a report: metrics → chart series → natural-language narrative (template-based 'AI' summary)."""
from datetime import datetime
from random import Random

from fastapi import HTTPException

from app.modules.reports.models import TEMPLATES, ReportIn, ScheduleIn, schedules

PERIOD_DAYS = {"7d": 7, "30d": 30, "90d": 90}
NEXT_RUN = {"daily": "Tomorrow 08:00", "weekly": "Monday 08:00", "monthly": "1st of next month"}


def _template(template_id: str) -> dict:
    t = next((t for t in TEMPLATES if t["id"] == template_id), None)
    if not t:
        raise HTTPException(404, "Unknown template")
    return t


def _fmt(unit: str, v: float) -> str:
    if unit == "$":
        return f"${v:,.0f}"
    return f"{v:,.1f}{unit}" if isinstance(v, float) and v < 100 else f"{v:,.0f}{unit}"


def generate(data: ReportIn) -> dict:
    t = _template(data.template_id)
    n = PERIOD_DAYS[data.period]
    r = Random(f"{data.template_id}{data.period}")
    scale = n / 30
    kpis = []
    for label, unit, base in t["kpis"]:
        value = base * (scale if unit in ("$", "") else 1) * r.uniform(0.92, 1.1)
        value = round(value, 1) if unit not in ("$", "") else round(value)
        kpis.append({"label": label, "value": _fmt(unit, value), "delta": round(r.uniform(-6, 18), 1)})
    points = min(n, 30)
    current = [round(100 + i * r.uniform(1, 3) + r.uniform(-12, 12)) for i in range(points)]
    previous = [round(v * r.uniform(0.78, 0.95)) for v in current]
    shares = [r.randint(10, 40) for _ in t["breakdown"]]
    top = t["breakdown"][shares.index(max(shares))]
    best, worst = max(kpis, key=lambda k: k["delta"]), min(kpis, key=lambda k: k["delta"])
    narrative = [
        f"{best['label']} was the standout metric, up {best['delta']}% versus the previous {n} days.",
        f"{top} drove the largest share ({round(max(shares) / sum(shares) * 100)}%) of activity this period.",
        (f"{worst['label']} declined {abs(worst['delta'])}% — worth a closer look before the next review."
         if worst["delta"] < 0 else f"Every headline metric improved; {worst['label']} grew the least (+{worst['delta']}%)."),
        "Recommendation: double down on the top channel and set an alert if the weakest metric drops another 5%.",
    ]
    return {"title": t["name"], "period": data.period, "generated_at": datetime.now().strftime("%b %d, %Y %H:%M"),
            "kpis": kpis, "series": {"labels": [f"D{i + 1}" for i in range(points)], "current": current, "previous": previous},
            "breakdown": {"labels": t["breakdown"], "values": shares}, "narrative": narrative}


def list_schedules() -> list[dict]:
    names = {t["id"]: t["name"] for t in TEMPLATES}
    return [{**s, "template": names[s["template_id"]]} for s in schedules.all()]


def create_schedule(data: ScheduleIn) -> dict:
    _template(data.template_id)
    schedules.add({"id": len(schedules.rows) + 1, **data.model_dump(), "next_run": NEXT_RUN[data.frequency]})
    return list_schedules()[0]


def delete_schedule(schedule_id: int) -> None:
    schedules.rows.remove(schedules.get_or_404(schedule_id))
