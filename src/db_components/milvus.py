from os import environ

from dotenv import load_dotenv
from pymilvus import MilvusClient, CollectionSchema

import src.utils.constants as consts
from src.db_components.create_schema import get_milvus_schema

# Load environment variables from .env file
load_dotenv()


def get_milvus_client() -> MilvusClient:
    """
    Creates and returns a Milvus client connection using environment variables.
    Requires MILVUS_URI and MILVUS_TOKEN environment variables to be set in .env file.
    """
    uri = environ.get("MILVUS_URI")
    token = environ.get("MILVUS_TOKEN")

    if not uri or not token:
        raise ValueError("MILVUS_URI and MILVUS_TOKEN environment variables must be set in .env file")

    client = MilvusClient(uri=uri, token=token)
    return client


def debug_milvus_state(client):
    print("📦 Databases:", client.list_databases())
    print("📚 Collections:", client.list_collections())


def create_collection(client: MilvusClient, collection_name: str, schema: CollectionSchema):
    """
    Creates a new collection in Milvus with the given name and schema.
    """
    try:
        client.create_collection(collection_name=collection_name, schema=schema)
        print(f"✅ Successfully created collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error while creating collection: {collection_name}", e)


def list_collections(client):
    return client.list_collections()


def create_index(client: MilvusClient, collection_name: str):
    """
    Creates an index on the cve_embedding field of the collection.
    """
    try:
        client.create_index(collection_name=collection_name, field_name="cve_embedding",
                            index_params={"index_type": "IVF_FLAT", "metric_type": "L2", "nlist": 1024})
        print(f"✅ Successfully created index on collection: {collection_name}")
    except Exception as e:
        print(f"❌ Error while creating index on collection {collection_name}: ", e)


def main():
    client = get_milvus_client()
    dbs = client.list_databases()
    print(f"Listing DBs: {dbs}")

    debug_milvus_state(client)

    schema = get_milvus_schema()

    print(f"Creating Collection: {consts.MILVUS_COLLECTION_NAME}")
    if consts.MILVUS_COLLECTION_NAME not in list_collections(client):
        create_collection(client=client, collection_name=consts.MILVUS_COLLECTION_NAME, schema=schema)
    else:
        print(f"Collection {consts.MILVUS_COLLECTION_NAME} already exists. Skipping creation.")

    # Create index after collection creation
    create_index(client=client, collection_name=consts.MILVUS_COLLECTION_NAME)

    collections = list_collections(client=client)
    print(f"Listing Collections: {collections}")


if __name__ == "__main__":
    main()
