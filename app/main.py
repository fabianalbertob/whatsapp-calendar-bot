import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqladmin import Admin, ModelView
from pywa.types import FlowRequest

from app.config.settings import settings
from app.controllers.whatsapp_controller import router as whatsapp_router
from app.database.session import engine, Base
from app.models.appointment import Appointment
from app.models.user import User
from app.services.whatsapp_service import wa
from app.services.whatsapp_flows import WhatsAppFlows
from app.utils.logger import logger

logger.info("📦 Importando módulos completado")

flows = WhatsAppFlows(wa)
logger.info("🔄 WhatsAppFlows inicializado")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Iniciando aplicación...")
    try:
        async with engine.begin() as conn:
            logger.info("🗄️ Creando tablas en la base de datos...")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("✅ Tablas creadas correctamente")
    except Exception as e:
        logger.error(f"❌ Error al crear tablas: {e}")
        raise
    
    logger.info("🚀 WhatsApp Bot iniciado correctamente")
    yield
    logger.info("🛑 Cerrando aplicación...")

app = FastAPI(title="WhatsApp Calendar Bot", lifespan=lifespan)
logger.info("✅ FastAPI app creada")

# Health check para Cloud Run
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "whatsapp-bot"}

@app.get("/")
async def root():
    return {"message": "WhatsApp Calendar Bot is running"}

# Panel Admin
admin = Admin(app, engine)

class AppointmentAdmin(ModelView, model=Appointment):
    column_list = "__all__"

class UserAdmin(ModelView, model=User):
    column_list = "__all__"

admin.add_view(AppointmentAdmin)
admin.add_view(UserAdmin)
logger.info("✅ Panel Admin configurado")

app.include_router(whatsapp_router, prefix="/whatsapp")
logger.info("✅ Router de WhatsApp incluido")

# Handler de mensajes
@wa.on_message()
async def handle_message(client, msg):
    text = msg.text.lower() if msg.text else ""
    if any(word in text for word in ["turno", "horario", "agendar", "reservar"]):
        flows.send_appointment_flow(msg.from_user)
    else:
        msg.reply_text("👋 Escribe *turno* para agendar una consulta.")

# Handler de Flows
@wa.on_flow_data()
async def on_flow_complete(client, flow_request: FlowRequest):
    await flows.handle_flow_completion(flow_request)

logger.info("✅ Handlers de WhatsApp registrados")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    logger.info(f"🌐 Iniciando servidor en puerto {port}")
    uvicorn.run(
        "app.main:app", 
        host="0.0.0.0", 
        port=port,
        reload=settings.debug
    )