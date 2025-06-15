from groq import Groq
from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

import src.utils.constants as consts
from src.llm.llm_utils import extract_info_via_llm
from src.llm.prompt_template import get_prompts

embedding_model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def get_embedding(text: str) -> list:
    formatted = f"Represent this CVE for retrieval: {text}"
    return embedding_model.encode(formatted).tolist()


def search_exact_cve_id(cve_id: str, intent: str, milvus_client: MilvusClient):
    results = []

    # 1. Try exact match with CVE ID if provided
    if cve_id:
        exact_match = milvus_client.query(
            collection_name=consts.MILVUS_COLLECTION_NAME,
            filter=f'cve_id == "{cve_id}"',
            output_fields=[
                "cve_id",
                "cve_description",
                "cve_published_date",
                "cve_severity",
                "cve_cwe",
                "cve_references",
            ],
        )
        if exact_match:
            results.extend(exact_match)

    if not results:
        return [], None, None, None
    else:
        # Use the first result for enrichment prompts
        top_cve = results[0]
        cve_id = top_cve.get("cve_id")
        description = top_cve.get("cve_description")
        prompts = get_prompts(cve_id=cve_id, description=description)
        return results, cve_id, intent, prompts


def search_vector_embedding(
    query_text: str,
    milvus_client: MilvusClient,
    groq_client: Groq,
    top_k: int = 10,
    severity_filter: str = None,
    cwe_filter: str = None,
):
    query_info = extract_info_via_llm(query=query_text, llm_client=groq_client)

    intent = query_info.get("intent", "general")

    results = []
    filters = []
    if severity_filter:
        filters.append(f'cve_severity == "{severity_filter.upper()}"')
    if cwe_filter:
        filters.append(f'cve_cwe like "{cwe_filter}%"')

    expr = " and ".join(filters) if filters else None

    query_embedding = get_embedding(query_text)
    vector_results = milvus_client.search(
        collection_name=consts.MILVUS_COLLECTION_NAME,
        data=[query_embedding],
        anns_field="cve_embedding",
        limit=top_k,
        filter=expr,
        search_params={"metric_type": "COSINE", "params": {"nprobe": 10}},
        output_fields=[
            "cve_id",
            "cve_description",
            "cve_published_date",
            "cve_severity",
            "cve_cwe",
            "cve_references",
        ],
    )
    results.extend(vector_results[0])

    if not results:
        return [], None, None, None

    # Use the first result for enrichment prompts
    top_cve = results[0]
    cve_id = top_cve.get("cve_id")
    description = top_cve.get("cve_description")
    prompts = get_prompts(cve_id=cve_id, description=description)

    return results, cve_id, intent, prompts
