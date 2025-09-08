# backend/app/tasks.py
from .models import MissedCall as MissedCallModel
from .db import SessionLocal
from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

def handle_missed_call(payload):

    db = SessionLocal()
    missed_call = MissedCallModel(caller_number=payload.caller_number, timestamp=payload.timestamp)
    db.add(missed_call)
    db.commit()
    db.close()

   
    if TWILIO_SID and TWILIO_AUTH_TOKEN:
        client.messages.create(
            body=f"You missed a call from {payload.caller_number}",
            from_=TWILIO_NUMBER,
            to=payload.caller_number
        )
