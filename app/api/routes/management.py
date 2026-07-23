# app/api/routes/management.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.api.deps import get_db, get_user_collection_name

router = APIRouter()

class DeleteUserCollectionRequest(BaseModel):
    user_id: str

class DeleteDocumentRequest(BaseModel):
    user_id: str
    source_filename: str

@router.post("/delete-collection")
async def delete_user_collection(req: DeleteUserCollectionRequest, request: Request):
    """
    Drops the entire single-collection for a specific user.
    Use with caution as this wipes their entire knowledge base.
    """
    db = get_db(request)
    collection_name = get_user_collection_name(req.user_id)
    try:
        db.drop_collection(collection_name)
        return {"response": f"Collection '{collection_name}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete collection: {str(e)}")

@router.post("/delete-document")
async def delete_document_by_source(req: DeleteDocumentRequest, request: Request):
    """
    Deletes specific documents within the user's single collection 
    based on the 'source' metadata field. 
    This is used when a user deletes a specific file from the frontend UI.
    """
    db = get_db(request)
    collection_name = get_user_collection_name(req.user_id)
    
    try:
        collection = db.get_collection(collection_name)
        # Delete all chunks where metadata.source matches the filename
        result = collection.delete_many({"metadata.source": req.source_filename})
        return {"response": f"Deleted {result.deleted_count} chunks for source '{req.source_filename}'."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")