from fastapi import APIRouter

from app.modules.chatbot import service
from app.modules.chatbot.models import ChatIn

router = APIRouter(prefix="/chatbot", tags=["AI Chatbot"])


@router.post("/message")
def message(body: ChatIn):
    return service.reply(body.message)


@router.get("/conversations")
def conversations():
    return service.inbox()
