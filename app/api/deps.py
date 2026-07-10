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
    try:
        return db.get_collection(collection_name)
    except Exception:
        # Auto-create if it doesn't exist yet (e.g., first chat before ingestion)
        return create_collection(db, collection_name)