import json
from typing import List

from sentence_transformers import SentenceTransformer

import src.utils.constants as consts

model = SentenceTransformer("BAAI/bge-base-en-v1.5")


def extract_fields(item) -> dict:
    cve = item.get("cve", {})
    meta = cve.get("CVE_data_meta", {})
    description_data = cve.get("description", {}).get("description_data", [])
    references_data = cve.get("references", {}).get("reference_data", [])
    problemtype_data = cve.get("problemtype", {}).get("problemtype_data", [])

    # Extract description in English
    cve_description = next((_["value"] for _ in description_data if _["lang"] == "en"), "")

    # Extract CWE
    cwe = next(
        (d.get("value", "") for pt in problemtype_data for d in pt.get("description", []) if d.get("lang") == "en"),
        "CWE-UNKNOWN", )

    # Extract unique references (deduplicated)
    references = list({ref["url"] for ref in references_data})

    # Parse impact safely
    impact_data = item.get("impact", {})
    base_metric_v3 = impact_data.get("baseMetricV3", {})
    cvss_v3 = base_metric_v3.get("cvssV3", {})
    cvss_score = cvss_v3.get("baseScore", None)
    severity = cvss_v3.get("baseSeverity", None)

    # Build embedding text (add this explicitly so your batch processing can access it)
    text_to_embed = f"{meta.get('ID', '')} - {cve_description} - CWE: {cwe}"

    # Return all original keys + the embedding text and embedding vector
    return {"cve_id": meta.get("ID", ""), "cve_assigned": meta.get("ASSIGNER", ""), "cve_description": cve_description,
            "cve_published_date": item.get("publishedDate", ""), "cve_impact_score": cvss_score,
            "cve_severity": severity, "cve_cwe": cwe, "cve_references": references, "text_to_embed": text_to_embed,
            "cve_embedding": model.encode(text_to_embed).tolist(), }


def process_all_cves_in_batches(file_path: str, batch_size: int = consts.SENTENCE_ENCODER_BATCH_SIZE) -> List[dict]:
    with open(file_path, "r") as f:
        data = json.load(f)

    all_cve_items = data.get("CVE_Items", [])
    enriched_records = []

    # Process in batches
    for i in range(0, len(all_cve_items), batch_size):
        batch_items = all_cve_items[i: i + batch_size]
        batch_records = [extract_fields(item) for item in batch_items]

        # Extract texts for batch embedding
        texts = [rec["text_to_embed"] for rec in batch_records]

        # Encode embeddings in batch for efficiency
        embeddings = model.encode(texts)

        # Add embeddings to records
        for rec, emb in zip(batch_records, embeddings):
            rec["cve_embedding"] = emb.tolist()
            rec.pop("text_to_embed", None)
            enriched_records.append(rec)

        print(f"Processed batch {i // batch_size + 1} / {(len(all_cve_items) + batch_size - 1) // batch_size}")

    return enriched_records
