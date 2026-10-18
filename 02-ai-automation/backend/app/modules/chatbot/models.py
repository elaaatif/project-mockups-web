from pydantic import BaseModel, Field

from app.core.common import Repository, rng


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    channel: str = "web"


# Knowledge base for the demo store "Lumen Home". In production this is a vector store + LLM.
INTENTS = [
    {"intent": "greeting", "keywords": ["hi", "hello", "hey", "morning", "evening"],
     "reply": "Hi there! 👋 I'm Nova, Lumen Home's assistant. I can track orders, handle returns, or answer product questions.",
     "suggestions": ["Track my order", "Return an item", "Shipping times"]},
    {"intent": "order_status", "keywords": ["order", "track", "where", "package", "delivery", "shipped"],
     "reply": "Happy to check that. Could you share your 5-digit order number? (Try 10482 or 10517)",
     "suggestions": ["Order 10482", "Order 10517"]},
    {"intent": "refund", "keywords": ["refund", "return", "money", "cancel", "broken", "damaged"],
     "reply": "You can return any item within 30 days for a full refund. I've generated a prepaid return label and emailed it to you — refunds land 3–5 days after we receive the parcel.",
     "suggestions": ["Talk to a human", "Shipping times"]},
    {"intent": "shipping", "keywords": ["shipping", "ship", "deliver", "days", "international", "cost"],
     "reply": "Standard shipping is free over $50 and takes 2–4 business days. Express (next day) is $9.90. We ship to 28 countries.",
     "suggestions": ["Track my order", "Return an item"]},
    {"intent": "product", "keywords": ["lamp", "sofa", "chair", "size", "material", "stock", "available", "colour", "color"],
     "reply": "Our Arc Floor Lamp is in stock in Brass and Matte Black (H 180cm, dimmable LED). Want me to reserve one or send the spec sheet?",
     "suggestions": ["Reserve one", "Send spec sheet"]},
    {"intent": "hours", "keywords": ["hours", "open", "close", "weekend", "sunday", "phone"],
     "reply": "Our support team is available Mon–Sat, 8:00–20:00. I'm here 24/7 for everything else!",
     "suggestions": ["Talk to a human"]},
    {"intent": "human", "keywords": ["human", "agent", "person", "someone", "representative", "complaint"],
     "reply": "No problem — I'm handing you over to Sarah from our care team. She'll see this whole conversation, so you won't need to repeat yourself.",
     "suggestions": [], "handoff": True},
    {"intent": "thanks", "keywords": ["thanks", "thank", "great", "perfect", "awesome"],
     "reply": "You're welcome! Anything else I can help with?", "suggestions": ["No, that's all"]},
]
ORDERS = {
    "10482": {"status": "Out for delivery", "eta": "today before 6 pm", "items": "Arc Floor Lamp (Brass)", "carrier": "DHL"},
    "10517": {"status": "Processing", "eta": "ships tomorrow", "items": "Linen Cushion Set ×2", "carrier": "UPS"},
    "10390": {"status": "Delivered", "eta": "delivered Oct 14", "items": "Oak Side Table", "carrier": "DHL"},
}

_CUSTOMERS = ["Emma Wilson", "Karim Aziz", "Lena Fischer", "Diego Ramos", "Aisha Bello", "Tom Becker",
              "Yuki Tanaka", "Sara Costa", "Ivan Petrov", "Nora Lindqvist"]
_TOPICS = ["Where is my order #10482?", "Can I return the oak table?", "Do you ship to Canada?",
           "Is the Arc lamp dimmable?", "I want to speak to someone", "Refund still not received",
           "Change delivery address", "Discount code not working"]
conversations = Repository([
    {"id": i + 1, "customer": c, "channel": rng.choice(["web", "whatsapp", "email"]), "last_message": rng.choice(_TOPICS),
     "status": rng.choice(["resolved_by_ai", "resolved_by_ai", "resolved_by_ai", "handed_off", "open"]),
     "messages": rng.randint(2, 14), "csat": rng.choice([5, 5, 4, 4, 3, None]), "minutes_ago": rng.randint(1, 600)}
    for i, c in enumerate(_CUSTOMERS)
])
