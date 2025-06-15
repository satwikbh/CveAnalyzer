import src.db_components.milvus as milvus

try:
    client = milvus.get_milvus_client()
    client.delete(collection_name="CVEs", filter="cve_id != ''")
except Exception as e:
    print(f"Error while creating a Milvus Client: {e}")
