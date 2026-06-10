from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
from app.utils.logger import logger
from app.config.settings import settings

class CalendarService:
    def __init__(self):
        self.service = self._build_service()

    def _build_service(self):
        # Implementa OAuth o Service Account según tu caso
        creds = Credentials.from_authorized_user_info(settings.google_credentials)
        if creds.expired:
            creds.refresh(Request())
        return build('calendar', 'v3', credentials=creds)

    def get_available_slots(self, days=7):
        try:
            now = datetime.utcnow().isoformat() + 'Z'
            end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId=settings.CALENDAR_ID,
                timeMin=now,
                timeMax=end,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            # Lógica para calcular slots libres (ej. 30min slots)
            logger.info("Slots recuperados", events_count=len(events_result.get('items', [])))
            return self._compute_free_slots(events_result.get('items', []))
        except Exception as e:
            logger.error("Error Google Calendar", error=str(e))
            raise

    def create_appointment(self, patient_info: dict, start_time: str):
        event = {
            'summary': f"Consulta {patient_info.get('name')}",
            'description': f"Tipo: {patient_info.get('type')}\nTel: {patient_info.get('phone')}",
            'start': {'dateTime': start_time, 'timeZone': 'America/Argentina/Buenos_Aires'},
            'end': {'dateTime': (datetime.fromisoformat(start_time.replace('Z','')) + timedelta(minutes=30)).isoformat() + 'Z', 'timeZone': 'America/Argentina/Buenos_Aires'},
        }
        try:
            event = self.service.events().insert(calendarId=settings.CALENDAR_ID, body=event).execute()
            logger.info("Evento creado", event_id=event['id'])
            return event
        except Exception as e:
            logger.error("Error creando evento", error=str(e))
            raise