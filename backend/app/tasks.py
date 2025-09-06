from .db import SessionLocal
from . import models

def handle_missed_call(payload):
    db = SessionLocal()
    try:
        # Save missed call to DB
        missed_call = models.MissedCall(
            device_id=payload.device_id,
            caller_number=payload.caller_number,
            receiver_number=payload.receiver_number
        )
        db.add(missed_call)
        db.commit()
        db.refresh(missed_call)
        print(f"Saved missed call from {payload.caller_number}")
        
        # TODO: Add SMS/WhatsApp logic here
        # send_sms(...)
        # send_whatsapp(...)
        
    finally:
        db.close()
