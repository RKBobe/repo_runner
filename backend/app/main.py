from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import ingest, chat

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], # Allow React (Vite uses 5173)
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods (POST, GET, etc)
    allow_headers=["*"], # Allow all headers
)

# register routes
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return { "status": "active", "message": "Repo Runner API is running" }
        

@app.get("/health")
def health_check():
    return {"status": "ok"}