from astrapy import Database, Collection
from astrapy.constants import VectorMetric
import astrapy

def create_collection(database: Database, collection_name: str) -> Collection:
    
    collection = database.create_collection(
        collection_name,
        metric=VectorMetric.COSINE,
        service=CollectionVectorServiceOptions(
            provider="nvidia",
            model_name="NV-Embed-QA",
        ),
    )
    # print(f"Created collection: {collection.full_name}")
    return collection

def insert(collection,collection_name,documents):
    # for doc in documents:
    #     doc["$vectorize"] = doc.get("vec", "")
    # print(documents)
    inserted = collection.insert_many(documents)
    return f"Inserted {len(inserted.inserted_ids)} items into '{collection_name}' collection."


def upload_data(database: Database, collection_name: str, documents: list) -> None:
    try:
        collection = database.get_collection(collection_name)
        res = insert(collection,collection_name,documents)
        return res
    except Exception:
        collection = create_collection(database, collection_name)
        res = insert(collection,collection_name,documents)
        return res
