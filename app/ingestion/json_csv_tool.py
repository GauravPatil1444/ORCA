# json_csv_tool.py
import os
import csv
import json
from app.ingestion.metadata_utils import create_metadata

def process_csv(file_path):
    json_data = []
    with open(file_path, mode="r", newline='', encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            json_data.append(row)
            
    source = os.path.basename(file_path)
    metadata = create_metadata(source, "csv", {})
    
    upload_data = []
    for item in json_data:
        upload_data.append({
            "data": str(item),
            "$vectorize": str(item),
            "metadata": metadata
        })
    return upload_data

def process_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        
    source = os.path.basename(file_path)
    metadata = create_metadata(source, "json", {})
    
    items = data if isinstance(data, list) else [data]
    upload_data = []
    for item in items:
        upload_data.append({
            "data": str(item),
            "$vectorize": str(item),
            "metadata": metadata
        })
    return upload_data