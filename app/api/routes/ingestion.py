# app/api/routes/ingestion.py
from fastapi import APIRouter, Request, File, UploadFile, Form, HTTPException
import os
import shutil
import re
from app.api.deps import get_db
from app.storage.astra_db import upload_data
from app.ingestion.advance_pdf_tool import process_pdf_regex
from app.ingestion.pdf_web_tool import process_web,process_pdf
from app.ingestion.json_csv_tool import process_csv, process_json
from app.ingestion.image_tool import process_image

router = APIRouter()

TEMP_DIR = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

FILE_CATEGORIES = {
    "application/pdf": "pdfs", "text/csv": "csvs", "application/json": "jsons",
    "image/jpeg": "images", "image/png": "images", "image/jpg": "images", "image/webp": "images"
}

@router.post("/upload")
async def upload_file(
    request: Request,
    user_id: str = Form(...),
    file: UploadFile = File(...), 
    pdfoption: str | None = Form(None), 
    regex: str | None = Form(None), 
    range_val: int | None = Form(None), 
    overlap: int | None = Form(None)
):
    db = get_db(request)
    content_type = file.content_type
    category = FILE_CATEGORIES.get(content_type)
    
    if not category:
        raise HTTPException(status_code=400, detail="Unsupported file type")
        
    file_path = os.path.join(TEMP_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Route to appropriate pipeline
    if category == "pdfs":
        docs = process_pdf_regex(file_path, regex) if pdfoption == "adv" else process_pdf(file_path, range_val, overlap)
    elif category == "csvs":
        docs = process_csv(file_path)
    elif category == "jsons":
        docs = process_json(file_path)
    elif category == "images":
        docs = process_image(file_path)
        
    res = upload_data(db, user_id, docs)
    
    try: os.remove(file_path)
    except PermissionError: pass
    
    return {"response": res}

@router.post("/webupload")
async def web_upload(request: Request, user_id: str = Form(...), link: str = Form(...), range_val: int = Form(...), overlap: int = Form(...)):
    db = get_db(request)
    docs = process_web(link, range_val, overlap)
    res = upload_data(db, user_id, docs)
    return {"response": res}