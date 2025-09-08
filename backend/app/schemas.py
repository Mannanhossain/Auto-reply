# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional

class MissedCall(BaseModel):
    caller_number: str
    timestamp: str

class MissedCallInDB(MissedCall):
    id: int
    caller_number: str
    timestamp: str

    class Config:
        from_attributes = True
