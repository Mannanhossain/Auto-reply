# backend/app/schemas.py
from pydantic import BaseModel

class MissedCall(BaseModel):
    caller_number: str
    timestamp: str
