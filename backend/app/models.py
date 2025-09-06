# backend/app/models.py
from sqlalchemy import Column, Integer, String
from .db import Base

class MissedCall(Base):
    __tablename__ = "missed_calls"

    id = Column(Integer, primary_key=True, index=True)
    caller_number = Column(String, index=True)
    timestamp = Column(String)
