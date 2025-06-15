from pymilvus import DataType, CollectionSchema, FieldSchema


def get_milvus_schema() -> CollectionSchema:
    """
    Creates and returns a Milvus collection schema for CVE data.
    """
    fields = [
        FieldSchema(
            name="cve_id",
            dtype=DataType.VARCHAR,
            max_length=20,
            is_primary=True,
        ),
        FieldSchema(name="cve_assigned", dtype=DataType.VARCHAR, max_length=500),
        FieldSchema(name="cve_description", dtype=DataType.VARCHAR, max_length=20000),
        FieldSchema(name="cve_published_date", dtype=DataType.VARCHAR, max_length=50),
        FieldSchema(name="cve_impact_score", dtype=DataType.FLOAT, nullable=True),
        FieldSchema(
            name="cve_severity", dtype=DataType.VARCHAR, max_length=64, nullable=True
        ),
        FieldSchema(name="cve_cwe", dtype=DataType.VARCHAR, max_length=64),
        FieldSchema(name="cve_references", dtype=DataType.JSON),
        FieldSchema(name="cve_embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    ]
    schema = CollectionSchema(fields=fields, description="CVE data collection")
    return schema
