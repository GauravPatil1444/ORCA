# app/storage/astra_db.py
import re
from astrapy import Database
from astrapy.constants import VectorMetric
from astrapy.info import CollectionDefinition, CollectionVectorOptions, VectorServiceOptions

def get_user_collection_name(user_id: str) -> str:
    """
    Sanitizes the authenticated user identifier to create a persistent, 
    unique single-collection name per user.
    """
    safe_id = re.sub(r'[^a-zA-Z0-9_]', '_', str(user_id))
    return f"user_{safe_id}"

def create_collection(database: Database, collection_name: str):
    """
    Creates a new vector collection using the Nvidia NV-EmbedQA-E5-V5 model 
    and Cosine similarity metric as defined in the architecture specs.
    """
    collection_definition = CollectionDefinition(
        vector=CollectionVectorOptions(
            metric=VectorMetric.COSINE,
            service=VectorServiceOptions(
                provider="nvidia",
                model_name="nvidia/nv-embedqa-e5-v5",
            )
        )
    )
    
    collection = database.create_collection(
        collection_name,
        definition=collection_definition,
    )
    print(f"* Created new single-collection: {collection.full_name}")
    return collection

def upload_data(database: Database, user_id: str, documents: list) -> str:
    """
    Targets the user's single collection, creating it if it doesn't exist,
    and inserts the processed documents (which already contain $vectorize and metadata).
    """
    collection_name = get_user_collection_name(user_id)
    
    try:
        collection = database.get_collection(collection_name)
    except Exception:
        # Auto-provision the collection on the first upload or chat interaction
        collection = create_collection(database, collection_name)
        
    if not documents:
        return "No documents provided for insertion."

    # AstraPy natively handles the 'data', '$vectorize', and 'metadata' root keys
    inserted = collection.insert_many(documents)
    return f"Successfully inserted {len(inserted.inserted_ids)} items into '{collection_name}'."