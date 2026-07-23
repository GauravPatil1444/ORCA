# app/storage/astra_db.py
import re
from astrapy import Database
from astrapy.constants import VectorMetric
from astrapy.info import CollectionDefinition

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
    and Cosine similarity metric.
    """
    collection_definition = (
        CollectionDefinition.builder()
        .set_vector_dimension(1024)  # NV-EmbedQA-E5-V5 output dimension
        .set_vector_metric(VectorMetric.COSINE)
        .set_vector_service(
            provider="nvidia",
            model_name="nvidia/nv-embedqa-e5-v5",
        )
        .build()
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
    and inserts the processed documents.
    """
    collection_name = get_user_collection_name(user_id)
    
    # 1. Fetch the actual list of collections from the server
    existing_collections = database.list_collection_names()
    
    # 2. Create if it doesn't exist, otherwise get the proxy
    if collection_name not in existing_collections:
        print(f"* Collection '{collection_name}' not found. Auto-provisioning...")
        collection = create_collection(database, collection_name)
    else:
        collection = database.get_collection(collection_name)
        
    if not documents:
        return "No documents provided for insertion."

    # 3. Insert documents
    inserted = collection.insert_many(documents)
    return f"Successfully inserted {len(inserted.inserted_ids)} items into '{collection_name}'."