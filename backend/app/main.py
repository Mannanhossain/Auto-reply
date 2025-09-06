# backend/app/main.py
from fastapi import FastAPI, HTTPException, Header
from . import models, schemas, tasks
from .db import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Missed Call Project API")

API_KEY = "supersecret"  # change your API key

@app.post("/webhook/missed_call")
def missed_call_webhook(payload: schemas.MissedCall, x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    tasks.handle_missed_call(payload)
    return {"status": "success", "caller_number": payload.caller_number}
