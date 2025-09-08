import os
from dotenv import load_dotenv
from twilio.rest import Client
from sqlalchemy.orm import Session
from .models import MissedCall
from datetime import datetime
import asyncio
import traceback

# Load .env from backend folder
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(dotenv_path)

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER")

# Initialize Twilio client safely
try:
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        print("Twilio client initialized successfully.")
    else:
        client = None
        print("Twilio client not created: Missing SID or Token.")
except Exception as e:
    client = None
    print(f"Error initializing Twilio client: {e}")
    traceback.print_exc()


async def send_whatsapp_message(to_number: str, message: str):
    """
    Send WhatsApp message asynchronously using Twilio.
    """
    if client:
        loop = asyncio.get_running_loop()
        try:
            sent_msg = await loop.run_in_executor(
                None,
                lambda: client.messages.create(
                    body=message,
                    from_=TWILIO_WHATSAPP_NUMBER,
                    to=to_number
                )
            )
            print(f"Message sent successfully! SID: {sent_msg.sid}")
            return sent_msg.sid
        except Exception as e:
            print(f"Error sending WhatsApp message: {e}")
            traceback.print_exc()
            return None
    else:
        print("Twilio client not initialized. Message not sent.")
        return None

def send_sms_message(to_number: str, message: str):
    """
    Sends a regular SMS message using Twilio.
    """
    if client:
        try:
            sent_msg = client.messages.create(
                body=message,
                from_=TWILIO_PHONE_NUMBER,
                to=to_number
            )
            print(f"SMS sent successfully! SID: {sent_msg.sid}")
            return sent_msg.sid
        except Exception as e:
            print(f"Error sending SMS message: {e}")
            traceback.print_exc()
            return None
    else:
        print("Twilio client not initialized. SMS not sent.")
        return None


async def log_missed_call(db: Session, caller_number: str):
    """
    Log a missed call and send notification.
    """
    try:
        print(f"DEBUG: Logging missed call for {caller_number}")
        # Assuming you have a 'phone_number' field in your MissedCall model
        missed_call = MissedCall(phone_number=caller_number) 
        db.add(missed_call)
        db.commit()
        db.refresh(missed_call)
        print(f"Missed call logged for {caller_number} at {missed_call.timestamp}")

        if ADMIN_PHONE_NUMBER:
            message = f"Missed call from {caller_number} at {missed_call.timestamp}"

            # THIS LINE SENDS THE SMS MESSAGE
            print(f"DEBUG: Sending SMS message to {ADMIN_PHONE_NUMBER}")
            send_sms_message(ADMIN_PHONE_NUMBER, message)
            
            # THIS LINE SENDS THE WHATSAPP MESSAGE
            print(f"DEBUG: Sending WhatsApp message to {ADMIN_PHONE_NUMBER}")
            await send_whatsapp_message(ADMIN_PHONE_NUMBER, message)
        else:
            print("ADMIN_PHONE_NUMBER not set in .env; message not sent.")

    except Exception as e:
        print(f"Error in log_missed_call: {e}")
        traceback.print_exc()
        raise
