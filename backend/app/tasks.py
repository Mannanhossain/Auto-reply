import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from dotenv import load_dotenv

load_dotenv()

# Twilio credentials from environment variables
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")  # Optional

async def send_notification(phone_number: str, timestamp: str) -> bool:
    """
    Send SMS and WhatsApp notification about the missed call
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, ADMIN_PHONE_NUMBER]):
        print("Twilio credentials not configured. Notification not sent.")
        return False
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message_body = f"Missed call from {phone_number} at {timestamp}. Please call back when available."
        
        # Send SMS
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )
        print(f"SMS sent. Message SID: {message.sid}")

        # Send WhatsApp (if configured)
        if TWILIO_WHATSAPP_NUMBER:
            try:
                wa_message = client.messages.create(
                    body=message_body,
                    from_="whatsapp:" + TWILIO_WHATSAPP_NUMBER,
                    to="whatsapp:" + ADMIN_PHONE_NUMBER
                )
                print(f"WhatsApp sent. Message SID: {wa_message.sid}")
            except TwilioRestException as e:
                print(f"WhatsApp error: {e}")

        return True
        
    except TwilioRestException as e:
        print(f"Twilio error: {e}")
        return False
    except Exception as e:
        print(f"Error sending notification: {e}")
        return False

# For testing: call the function and see output
if __name__ == "__main__":
    import asyncio
    asyncio.run(send_notification("+1234567890", "2025-09-05 12:00:00"))