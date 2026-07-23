# app/api/deps.py
from fastapi import Request, HTTPException
from astrapy import Database
from app.storage.astra_db import get_user_collection_name, create_collection

def get_db(request: Request) -> Database:
    db = request.app.state.db
    if not db:
        raise HTTPException(status_code=500, detail="Database connection is not available")
    return db

def get_user_collection(request: Request, user_id: str):
    """Resolves the single collection for the authenticated user."""
    db = get_db(request)
    collection_name = get_user_collection_name(user_id)
    
    # Check actual server state instead of relying on the get_collection() proxy
    existing_collections = db.list_collection_names()
    
    if collection_name not in existing_collections:
        print(f"* Auto-provisioning collection '{collection_name}' for chat...")
        return create_collection(db, collection_name)
        
    return db.get_collection(collection_name)