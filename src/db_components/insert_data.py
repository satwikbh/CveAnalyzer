import src.utils.constants as consts


def insert_data_into_db(client, data):
    """
    Inserts formatted CVE records into Milvus.
    Each record must be a dict with the correct schema fields.
    """
    if not data:
        print("⚠️ No data to insert. Skipping.")
        return

    # Validate embedding dimension
    expected_dim = 768
    for i, item in enumerate(data):
        if len(item["cve_embedding"]) != expected_dim:
            raise ValueError(
                f"Embedding dimension mismatch at index {i}: expected {expected_dim}, got {len(item['cve_embedding'])}")

    try:
        client.insert(collection_name=consts.MILVUS_COLLECTION_NAME, data=data)
        print(f"✅ Successfully inserted {len(data)} records into {consts.MILVUS_COLLECTION_NAME}")
    except Exception as e:
        print(f"❌ Error inserting into collection {consts.MILVUS_COLLECTION_NAME}:\n{e}")
