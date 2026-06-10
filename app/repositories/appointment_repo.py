from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.models.appointment import Appointment
from typing import Dict, List

class AppointmentRepository:
    async def create(self, data: Dict) -> Appointment:
        async with get_db() as session:
            appointment = Appointment(**data)
            session.add(appointment)
            await session.commit()
            await session.refresh(appointment)
            return appointment

    async def get_by_phone(self, phone: str) -> List[Appointment]:
        async with get_db() as session:
            result = await session.execute(
                select(Appointment).where(Appointment.patient_phone == phone)
            )
            return result.scalars().all()