# upload.py
import re
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.info import CollectionDefinition, CollectionVectorOptions, VectorServiceOptions
from dotenv import load_dotenv
import os

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")

def get_user_collection_name(user_id: str) -> str:
    """Sanitizes the authenticated user identifier to create a persistent, unique collection name."""
    return f"user_{re.sub(r'[^a-zA-Z0-9_]', '_', str(user_id))}"

def create_collection(database, collection_name: str):
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
    print(f"* Collection: {collection.full_name}\n")
    return collection

def insert(collection, documents):
    # AstraPy natively handles the 'data', '$vectorize', and 'metadata' root keys
    inserted = collection.insert_many(documents)
    return f"Inserted {len(inserted.inserted_ids)} items."

def upload_data(database, user_id: str, documents: list) -> str:
    """Targets the single user collection, creating it if it doesn't exist."""
    collection_name = get_user_collection_name(user_id)
    try:
        collection = database.get_collection(collection_name)
    except Exception:
        collection = create_collection(database, collection_name)
        
    return insert(collection, documents)