from fastapi import FastAPI
from .database import engine
from .models import Base
from .auth import router as auth_router

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}