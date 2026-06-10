from datetime import datetime, timedelta
from typing import List, Dict
from app.repositories.appointment_repo import AppointmentRepository
from app.services.calendar_service import CalendarService
from app.utils.logger import logger
from app.models.appointment import Appointment

class AppointmentService:
    def __init__(self):
        self.repo = AppointmentRepository()
        self.calendar = CalendarService()

    async def get_available_slots(self, days: int = 7) -> List[str]:
        try:
            # Obtener eventos de Google Calendar
            events = await self.calendar.get_events(days=days)
            busy_times = [(e['start'], e['end']) for e in events]

            # Generar slots cada 30 minutos (ejemplo de 9:00 a 18:00)
            slots = []
            start_date = datetime.utcnow().replace(hour=9, minute=0, second=0, microsecond=0)
            
            for day in range(days):
                current = start_date + timedelta(days=day)
                for hour in range(9, 18):
                    for minute in [0, 30]:
                        slot_start = current.replace(hour=hour, minute=minute)
                        slot_end = slot_start + timedelta(minutes=30)
                        
                        if not self._is_slot_busy(slot_start, slot_end, busy_times):
                            slots.append(slot_start.strftime("%d/%m/%Y %H:%M"))
            
            return slots[:15]  # Limitar cantidad mostrada
        except Exception as e:
            logger.error("Error obteniendo slots", error=str(e))
            return []

    def _is_slot_busy(self, start, end, busy_times):
        for b_start, b_end in busy_times:
            if not (end <= b_start or start >= b_end):
                return True
        return False

    async def create_appointment(self, patient_data: Dict) -> Appointment:
        try:
            appointment = await self.repo.create(patient_data)
            
            # Sincronizar con Google Calendar
            await self.calendar.create_event(appointment)
            
            logger.info("Turno creado", phone=patient_data['patient_phone'])
            return appointment
        except Exception as e:
            logger.error("Error creando turno", error=str(e))
            raise

    async def get_appointments_by_phone(self, phone: str):
        return await self.repo.get_by_phone(phone)