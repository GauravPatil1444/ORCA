# image_tool.py
import os
import requests
from metadata_utils import create_metadata

def imageprocess(file_path):
    with open(file_path, "rb") as img_file:
        files = {"file": (os.path.basename(file_path), img_file, "image/png")}
        response = requests.post('https://ocr-1-0-0.onrender.com/ocr/', files=files)
        
    json_response = response.json()
    extracted_text = json_response.get("text", "")
    
    uploadDocs = []
    if extracted_text:
        source = os.path.basename(file_path)
        metadata = create_metadata(source, "image", {})
        uploadDocs.append({
            "data": extracted_text,
            "$vectorize": extracted_text,
            "metadata": metadata
        })
    return uploadDocs