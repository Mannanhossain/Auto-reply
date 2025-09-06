# app/main.py

import os
from fastapi import FastAPI, HTTPException, Header
from . import models, schemas, tasks
from .db import engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Missed Call Project API")

# Use environment variable for API key
API_KEY = os.getenv("API_KEY", "supersecret")  # default fallback

@app.post("/webhook/missed_call")
def missed_call_webhook(payload: schemas.MissedCall, x_api_key: str = Header(...)):
    """
    Endpoint to receive missed call events.
    Expects X-API-KEY header for authentication.
    """
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Call task to handle missed call (send SMS/WhatsApp)
    tasks.handle_missed_call(payload)

    return {
        "status": "success",
        "caller_number": payload.caller_number,
        "receiver_number": payload.receiver_number
    }

# Optional: simple root endpoint
@app.get("/")
def root():
    return {"message": "Missed Call Backend is running!"}
