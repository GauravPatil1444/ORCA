from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from astrapy import Database
from upload import upload_data
from astra_agent import Agent
from astrapy.client import DataAPIClient
import shutil
from pdf_web_tool import pdfprocess
from advance_pdf_tool import adv_pdf
import re
from json_csv_tool import csvprocess
from json_csv_tool import jsonprocess
from pdf_web_tool import webprocess
from OWST import embed
from image_tool import imageprocess
from starlette.responses import HTMLResponse

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

def document_type(file_path,category,pdfoption,range,regex,overlap):

    if category=="pdfs":
        if pdfoption=="adv":
            return adv_pdf(file_path,regex)
        else:
            return pdfprocess(file_path,range,overlap)
    
    elif category=="csvs":
        return csvprocess(file_path)
    
    elif category=="jsons":
        return jsonprocess(file_path)
    
    elif category=="images":
        return imageprocess(file_path)
    



@app.post("/upload")
async def upload(file: UploadFile = File(...),collection_name: str = Form(...),pdfoption: str|None = Form(...),regex: str|None = Form(...),range: int|None = Form(...),overlap: int|None = Form(...)):
    try:
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '_', collection_name)
        content_type = file.content_type
        category = FILE_CATEGORIES.get(content_type)

        if not category:
            return {"error": "Unsupported file type"}
        
        file_path = os.path.join('./temp', file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    
        uploadDocs = document_type(file_path,category,pdfoption,range,regex,overlap)
        db = get_db()
        res = upload_data(db,collection_name,uploadDocs)
        os.remove(f'./temp/{file.filename}')
        return {"response":res}
    except Exception as e:
        return {"error": "Something went wrong!","reason":str(e)}

class DeleteData(BaseModel):
    collection_name: str

@app.post("/delete")
def delete_collection(req: DeleteData, db: Database = Depends(get_db)):
    result = db.drop_collection(req.collection_name)
    return result

class searchData(BaseModel):
    data: str|None
    collection_name: str
    prompt: str|None

@app.post("/search")
def ask_orca(req: searchData, db: Database = Depends(get_db)):
    collection_name = re.sub(r'[^a-zA-Z0-9_]', '_', req.collection_name)
    try:
        collection = db.get_collection(collection_name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid collection: {str(e)}")
    
    response = Agent(req.data, collection, req.prompt)
    
    return {"response": response}


class OWSTData(BaseModel):
    link: str
    query: str
    classes_to_remove: str|None

@app.get("/owst")
def owst(link: str, query: str, classes_to_remove: str):
    try:
        res = embed(link,query,classes_to_remove.split(','))
        return HTMLResponse(content=res)
    except Exception as e:
        return e

class webData(BaseModel):
    link: str
    collection_name: str
    range: int
    overlap:int

@app.post("/webupload")
async def web(req: webData, db: Database = Depends(get_db)):
    try:
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '_', req.collection_name)

        upload_docs = webprocess(req.link,req.range,req.overlap)
        response = upload_data(db,collection_name,upload_docs)
        
        return {"response": response}
    
    except Exception as e:
        return{"error":e}


@app.get("/")
def hello_orca():
    return "Welcome to ORCA - this is API Gateway and services are running successfully!"
