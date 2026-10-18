from random import Random

from app.modules.workflows.models import WorkflowIn, workflows

SAMPLE_OUTPUT = {
    "ai_extract": "Extracted 8 fields (vendor, total $6,240.00, due Nov 12) · confidence 0.96",
    "ai_classify": "Intent: purchase_inquiry · budget: $2–5k · confidence 0.93",
    "ai_reply": "Drafted 64-word reply in customer's language (EN)",
    "ai_summarize": "Summary: revenue +8.4%, 3 risks flagged",
    "condition": "Condition evaluated → TRUE branch",
    "send_whatsapp": "Message delivered to +44 77•• ••0123 ✓✓",
    "send_email": "Email queued via SMTP · message-id <a81f@autom8>",
    "crm_update": "Lead #48213 created in HubSpot",
    "sheet_append": "Row 1,204 appended to 'Fulfilment'",
    "erp_post": "POST /bills → 201 Created",
    "notify_slack": "Posted to #finance-approvals",
}


def toggle(workflow_id: int) -> dict:
    wf = workflows.get_or_404(workflow_id)
    wf["enabled"] = not wf["enabled"]
    return wf


def create(data: WorkflowIn) -> dict:
    return workflows.add({"id": max(w["id"] for w in workflows.all()) + 1, **data.model_dump(), "enabled": True,
                          "runs": 0, "success_rate": 100.0, "last_run": "never"})


def test_run(workflow_id: int) -> dict:
    wf = workflows.get_or_404(workflow_id)
    r = Random(workflow_id + wf["runs"])
    log = [{"label": wf["trigger"]["label"], "type": "trigger", "status": "ok", "duration_ms": r.randint(5, 30), "output": "Trigger fired with test payload"}]
    for step in wf["steps"]:
        ms = r.randint(600, 2200) if step["type"].startswith("ai_") else r.randint(40, 400)
        log.append({"label": step["label"], "type": step["type"], "status": "ok", "duration_ms": ms,
                    "output": SAMPLE_OUTPUT.get(step["type"], "Done")})
    wf["runs"] += 1
    wf["last_run"] = "just now"
    return {"workflow_id": workflow_id, "log": log, "total_ms": sum(s["duration_ms"] for s in log)}
