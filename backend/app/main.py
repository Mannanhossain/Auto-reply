from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import asyncio

from . import models, schemas, tasks
from .db import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Missed Call Project API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Missed Call Project API is running!"}

# Health check
@app.get("/health/")
async def health_check():
    return {"status": "healthy", "service": "missed-call-api"}

# POST missed call
@app.post("/missed-call/", response_model=schemas.MissedCallResponse)
async def handle_missed_call(request: schemas.MissedCallRequest, db: Session = Depends(get_db)):
    try:
        db_call = models.MissedCall(
            phone_number=request.phone_number,
            timestamp=request.timestamp,
            status="received"
        )
        db.add(db_call)
        db.commit()
        db.refresh(db_call)

        # Send notification asynchronously
        loop = asyncio.get_event_loop()
        sent = await loop.run_in_executor(None, tasks.send_notification, request.phone_number, request.timestamp)

        if sent:
            db_call.status = "notification_sent"
        else:
            db_call.status = "notification_failed"
        db.commit()
        db.refresh(db_call)

        return {
            "id": db_call.id,
            "status": db_call.status,
            "message": "Missed call recorded successfully"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET missed calls
@app.get("/missed-calls/", response_model=List[schemas.MissedCall])
async def get_missed_calls(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.MissedCall).offset(skip).limit(limit).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
