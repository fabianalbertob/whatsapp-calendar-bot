from pywa import WhatsApp
from pywa.types import FlowRequest, FlowResponse
from app.services.appointment_service import AppointmentService
from app.utils.logger import logger
from datetime import datetime

# Instancia del servicio
appointment_service = AppointmentService()


class WhatsAppFlows:
    def __init__(self, wa_client: WhatsApp):
        self.wa = wa_client

    def send_appointment_flow(self, to: str):
        """Envía el Flow interactivo para agendar turno"""
        try:
            # Placeholder - En producción obtén slots reales desde la base de datos
            slots = ["10/06/2026 09:00", "10/06/2026 09:30", "10/06/2026 10:00"]

            # Aquí iría el Flow creado en Meta Flow Builder
            self.wa.send_flow(
                to=to,
                flow_id="TU_FLOW_ID_AQUI",   # ← Reemplaza con el ID real del Flow de Meta
                header_text="📅 Agendar Consulta",
                body_text="Completa los datos para reservar tu turno",
                data={
                    "available_slots": [{"id": s, "title": s} for s in slots]
                }
            )
            logger.info(f"Flow enviado correctamente a {to}")
        except Exception as e:
            logger.error(f"Error enviando Flow: {str(e)}")
            self.wa.send_text(to=to, text="Lo siento, hubo un error. Inténtalo más tarde.")

    async def handle_flow_completion(self, flow_request: FlowRequest):
        """Procesa la respuesta del Flow"""
        try:
            data = flow_request.data
            patient_data = {
                "patient_name": data.get("patient_name"),
                "patient_phone": flow_request.from_user,
                "appointment_type": "consulta_general",
                "payment_type": data.get("payment_type", "particular"),
                "start_time": datetime.strptime(data.get("selected_slot"), "%d/%m/%Y %H:%M"),
            }

            await appointment_service.create_appointment(patient_data)

            # Respuesta de éxito dentro de WhatsApp
            flow_request.reply(
                FlowResponse(
                    screen="success_screen",
                    data={"message": f"✅ Turno confirmado para {data.get('selected_slot')}"}
                )
            )
            logger.info(f"Turno agendado vía Flow para {flow_request.from_user}")
        except Exception as e:
            logger.error(f"Error procesando Flow: {str(e)}")
            flow_request.reply_error("Hubo un problema al guardar el turno. Intenta nuevamente.")