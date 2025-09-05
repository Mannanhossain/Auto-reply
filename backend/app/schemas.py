from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MissedCallRequest(BaseModel):
    phone_number: str
    timestamp: datetime

class MissedCallResponse(BaseModel):
    id: int
    status: str
    message: str

class MissedCall(BaseModel):
    id: int
    phone_number: str
    timestamp: datetime
    status: str

    class Config:
        orm_mode = True