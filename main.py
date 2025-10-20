from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr
from datetime import datetime
import os
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import PlainTextResponse
import time
import httpx
import asyncio
from typing import Optional
from prometheus_fastapi_instrumentator import Instrumentator

#for Prometheus metrics
app = FastAPI()
Instrumentator().instrument(app).expose(app)    

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Webhook configuration
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Prometheus metrics
REQUEST_COUNT = Counter('http_request_total', 'Total HTTP requests', ['method', 'path'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration', ['method', 'path'])

app = FastAPI(title="AutoBud Contact API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://autobud.co", "https://autobud.co", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Models
class ContactSubmission(Base):
    __tablename__ = os.getenv("TABLE_NAME", "contact_submissions")
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    company = Column(String(255), nullable=True)
    message = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

# Pydantic Models
class ContactFormData(BaseModel):
    name: str
    email: EmailStr
    company: str = ""
    message: str

class ContactResponse(BaseModel):
    id: int
    name: str
    email: str
    company: str
    message: str
    submitted_at: datetime
    
    class Config:
        from_attributes = True

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables
Base.metadata.create_all(bind=engine)

# Helper function to send webhook
async def send_webhook(data: dict) -> Optional[dict]:
    """
    Send form data to webhook URL as JSON.
    Returns response data if successful, None if webhook URL not configured or on error.
    """
    if not WEBHOOK_URL:
        return None

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                WEBHOOK_URL,
                json=data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return {"status": "success", "status_code": response.status_code}
    except httpx.HTTPError as e:
        # Log error but don't fail the form submission
        print(f"Webhook error: {str(e)}")
        return {"status": "error", "error": str(e)}
    except Exception as e:
        print(f"Unexpected webhook error: {str(e)}")
        return {"status": "error", "error": str(e)}

# Middleware for metrics
@app.middleware("http")
async def add_prometheus_metrics(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, path=request.url.path).inc()
    REQUEST_DURATION.labels(method=request.method, path=request.url.path).observe(duration)
    
    return response

@app.get("/")
def read_root():
    return {"message": "AutoBud Contact API is running"}

@app.post("/api/contact", response_model=ContactResponse)
async def submit_contact_form(contact_data: ContactFormData, db: Session = Depends(get_db)):
    try:
        # Create new contact submission
        db_contact = ContactSubmission(
            name=contact_data.name,
            email=contact_data.email,
            company=contact_data.company,
            message=contact_data.message
        )

        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)

        # Prepare webhook payload
        webhook_payload = {
            "id": db_contact.id,
            "name": db_contact.name,
            "email": db_contact.email,
            "company": db_contact.company,
            "message": db_contact.message,
            "submitted_at": db_contact.submitted_at.isoformat()
        }

        # Send to webhook asynchronously (non-blocking)
        await send_webhook(webhook_payload)

        return db_contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save contact form: {str(e)}")

@app.get("/api/contacts", response_model=list[ContactResponse])
def get_all_contacts(db: Session = Depends(get_db)):
    contacts = db.query(ContactSubmission).order_by(ContactSubmission.submitted_at.desc()).all()
    return contacts

@app.get("/api/contacts/{contact_id}", response_model=ContactResponse)
def get_contact_by_id(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(ContactSubmission).filter(ContactSubmission.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.get("/metrics")
def get_metrics():
    return PlainTextResponse(generate_latest())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)