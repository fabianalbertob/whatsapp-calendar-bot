from fastapi import APIRouter, Request
from app.services.whatsapp_service import wa
from app.services.whatsapp_flows import WhatsAppFlows

router = APIRouter()
flows = WhatsAppFlows(wa)

@router.get("/webhook")
async def verify_webhook(request: Request):
    return await wa.verify_webhook(request)

@router.post("/webhook")
async def webhook(request: Request):
    return await wa.process_webhook(request)