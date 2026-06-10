from pywa import WhatsApp
from app.config.settings import settings

wa = WhatsApp(
    token=settings.whatsapp_access_token,
    phone_id=settings.whatsapp_phone_number_id,
    verify_token=settings.whatsapp_webhook_verify_token,
)