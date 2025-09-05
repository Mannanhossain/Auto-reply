from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .db import Base

class MissedCall(Base):
    __tablename__ = "missed_calls"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, index=True)
    timestamp = Column(DateTime, default=func.now())
    status = Column(String, default="received")  # received, notification_sent, notification_failed