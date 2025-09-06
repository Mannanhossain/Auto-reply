from pydantic import BaseModel

class MissedCall(BaseModel):
    device_id: str
    caller_number: str
    receiver_number: str
