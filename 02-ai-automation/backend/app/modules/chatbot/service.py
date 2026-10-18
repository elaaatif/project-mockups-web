"""Tiny intent classifier — keyword overlap + entity extraction. Swap `classify` for an LLM call in production."""
import re
import time

from app.modules.chatbot.models import INTENTS, ORDERS, conversations

FALLBACK = {"intent": "fallback", "reply": "I'm not 100% sure I understood. I can track orders, explain returns and shipping, or connect you with a teammate.",
            "suggestions": ["Track my order", "Return an item", "Talk to a human"]}


def classify(message: str) -> tuple[dict, float]:
    words = set(re.findall(r"[a-z]+", message.lower()))
    best, best_score = FALLBACK, 0.0
    for intent in INTENTS:
        hits = sum(1 for k in intent["keywords"] if k in words or (" " in k and k in message.lower()))
        score = hits / (len(intent["keywords"]) ** 0.5)
        if score > best_score:
            best, best_score = intent, score
    return best, min(0.99, 0.55 + best_score * 0.4) if best_score else 0.32


def reply(message: str) -> dict:
    started = time.perf_counter()
    order_no = re.search(r"\b(\d{5})\b", message)
    if order_no:
        no = order_no.group(1)
        order = ORDERS.get(no)
        text = (f"Order #{no} — {order['items']} — is **{order['status']}** with {order['carrier']}, {order['eta']}."
                if order else f"I couldn't find order #{no}. Double-check the number from your confirmation email?")
        result = {"intent": "order_status", "reply": text, "suggestions": ["Return an item", "Thanks!"],
                  "entities": {"order_number": no}, "confidence": 0.97 if order else 0.71}
    else:
        intent, confidence = classify(message)
        result = {"intent": intent["intent"], "reply": intent["reply"], "suggestions": intent.get("suggestions", []),
                  "entities": {}, "confidence": round(confidence, 2), "handoff": intent.get("handoff", False)}
    result["latency_ms"] = round((time.perf_counter() - started) * 1000 + 180, 0)
    return result


def inbox() -> dict:
    rows = sorted(conversations.all(), key=lambda c: c["minutes_ago"])
    resolved = sum(1 for c in rows if c["status"] == "resolved_by_ai")
    rated = [c["csat"] for c in rows if c["csat"]]
    return {"conversations": rows, "stats": {"total": len(rows), "ai_resolution": round(resolved / len(rows) * 100),
                                             "csat": round(sum(rated) / len(rated), 1), "avg_response_s": 1.4}}
