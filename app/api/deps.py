# app/api/deps.py
import time
from fastapi import Request, HTTPException
from astrapy import DataAPIClient, Database
from astrapy.exceptions import DataAPIHttpException
from app.core.config import get_settings

settings = get_settings()
client = DataAPIClient(settings.ASTRA_DB_APPLICATION_TOKEN)
db = client.get_database(settings.ASTRA_DB_API_ENDPOINT)

def get_db(request: Request) -> Database:
    db = request.app.state.db
    if not db:
        raise HTTPException(status_code=500, detail="Database connection is not available")
    return db


def get_user_collection(request: Request, user_id: str):
    # Sanitize user_id to match your collection naming convention
    collection_name = f"user_{user_id.replace('-', '_')}" 
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 1. Ping the DB to ensure it's awake (triggers wake-up if hibernating)
            db.list_collection_names() 
            
            # 2. Get or create the collection
            collection = db.get_collection(collection_name)
            return collection
            
        except (DataAPIHttpException, Exception) as e:
            # Catch the 503 Hibernation Error
            if "503" in str(e) and attempt < max_retries - 1:
                print(f" [Astra DB] Hibernating/Waking up. Retrying in 5s... (Attempt {attempt + 1})")
                time.sleep(5) # Wait for the DB to fully boot
                continue
            
            # If it's a different error, or retries are exhausted, raise it
            print(f" [Astra DB] Failed to connect: {e}")
            raise HTTPException(
                status_code=503, 
                detail="Knowledge base is currently waking up from hibernation. Please try again in 5 seconds."
            )