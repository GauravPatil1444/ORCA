from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
from typing import List, Dict
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from astrapy import Database
from upload import upload_data
from astra_agent import Agent
from astrapy.client import DataAPIClient
import shutil
from pdf_tool import pdfprocess

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

FILE_CATEGORIES = {
    "application/pdf": "pdfs",
    "text/csv": "csvs",
    "application/json": "jsons",
    "image/jpeg": "images",
    "image/png": "images",
    "image/jpg": "images",
    "image/webp": "images"
}

@app.post("/upload")
async def upload(file: UploadFile = File(...),collection_name: str = Form(...)):
    try:
        content_type = file.content_type
        category = FILE_CATEGORIES.get(content_type)

        if not category:
            return {"error": "Unsupported file type"}
        
        file_path = os.path.join('./temp', file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    
        uploadDocs = pdfprocess(file.filename)
        db = get_db()
        res = upload_data(db,collection_name,uploadDocs)
        os.remove(f'./temp/{file.filename}')
        return {"response":res}
    except:
        return {"error": "Something went wrong!"}


class searchData(BaseModel):
    data: str
    collection_name: str

@app.post("/search")
async def ask_orca(req: searchData, db: Database = Depends(get_db)):
    try:
        collection = db.get_collection(req.collection_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid collection: {str(e)}")

    response = Agent(req.data, collection)
    
    return {"response": response}


@app.get("/")
def hello_world():
    return "Welcome to ORCA - services are running successfully!"
