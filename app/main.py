# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from astrapy import DataAPIClient
from app.core.config import get_settings
from app.api.routes import chat, ingestion, management, owst

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Astra DB connection
    client = DataAPIClient(settings.ASTRA_DB_APPLICATION_TOKEN)
    app.state.db = client.get_database(settings.ASTRA_DB_API_ENDPOINT)
    print("* Connected to Astra DB successfully.")
    yield
    # Shutdown
    app.state.db = None

app = FastAPI(title="ORCA Agentic Backend", lifespan=lifespan)

# CORS Configuration (Update origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Modular Routers
app.include_router(chat.router, prefix="/v2", tags=["Chat"])
app.include_router(ingestion.router, tags=["Ingestion"])
app.include_router(management.router, tags=["Management"])
app.include_router(owst.router, tags=["OWST"])

@app.get("/")
def health_check():
    return {"status": "ORCA Agentic Services are running successfully!"}