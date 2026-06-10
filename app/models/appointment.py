from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class Appointment(Base):
    __tablename__ = "appointments"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String, nullable=False)
    patient_phone = Column(String, nullable=False, index=True)
    appointment_type = Column(String)  # consulta, control, etc.
    payment_type = Column(String)      # particular, obra_social
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(String, default="confirmed")  # confirmed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)