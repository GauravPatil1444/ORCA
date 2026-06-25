from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.info import CollectionDefinition, CollectionVectorOptions, VectorServiceOptions
from dotenv import load_dotenv
import os

load_dotenv()
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")


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


def insert(collection, collection_name, documents):
    inserted = collection.insert_many(documents)
    return f"Inserted {len(inserted.inserted_ids)} items into '{collection_name}' collection."


def upload_data(database, collection_name: str, documents: list) -> None: 
    try:
        collection = database.get_collection(collection_name)
        res = insert(collection, collection_name, documents)
        return res
    except Exception:
        collection = create_collection(database, collection_name)
        res = insert(collection, collection_name, documents)
        return res