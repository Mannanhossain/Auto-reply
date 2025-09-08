from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import get_db
from .tasks import log_missed_call
from pydantic import BaseModel
import traceback

app = FastAPI(title="Missed Call API Async + Pydantic + Safe")

# Pydantic request model
class MissedCallRequest(BaseModel):
    caller_number: str


@app.post("/missed-call/")
async def create_missed_call(request: MissedCallRequest, db: Session = Depends(get_db)):
    """
    Log missed call and send WhatsApp notification asynchronously.
    """
    try:
        await log_missed_call(db, request.caller_number)
        return {"message": f"Missed call from {request.caller_number} logged and notification sent."}
    except Exception as e:
        error_details = traceback.format_exc()
        print("ERROR in create_missed_call:\n", error_details)
        raise HTTPException(status_code=500, detail=str(e))
