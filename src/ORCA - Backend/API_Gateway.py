from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from astrapy import Database
from upload import upload_data
from Agent import Agent
from astrapy.client import DataAPIClient

load_dotenv()

ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

def connect_to_database() -> Database:
    client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
    database = client.get_database(ASTRA_DB_API_ENDPOINT)
    print(f"Connected to database {database.info().name}")
    return database

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = connect_to_database()
    yield
    app.state.db = None  

app = FastAPI(lifespan=lifespan)

def get_db():
    if not app.state.db:
        raise HTTPException(status_code=500, detail="Database connection is not available")
    return app.state.db

class UploadRequest(BaseModel):
    collection_name: str
    data: List[Dict]

@app.post("/upload")
async def upload(upload_request: UploadRequest):
    """
    API endpoint to create a collection and upload client-provided data.
    """
    db = get_db()
    try:
        upload_data(db, upload_request.collection_name, upload_request.data)
        return {"message": "Data uploaded successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class LegalQuery(BaseModel):
    data: str
    collection_name: str

@app.post("/search")
async def ask_orca(query: LegalQuery, db: Database = Depends(get_db)):
    try:
        collection = db.get_collection(query.collection_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid collection: {str(e)}")

    response = Agent(query.data, collection)
    
    return {"response": response}


@app.get("/")
def hello_world():
    return "Welcome to ORCA - services are running successfully!"
