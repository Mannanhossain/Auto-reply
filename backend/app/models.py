from sqlalchemy import Column, Integer, String, DateTime
from .db import Base
from datetime import datetime

class MissedCall(Base):
    __tablename__ = "missed_calls"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)  # Must match the keyword
    timestamp = Column(DateTime, default=datetime.utcnow)
