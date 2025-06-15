from typing import TypedDict, Optional, Literal, List

from langgraph.graph import StateGraph, END

from src.db_components.milvus import get_milvus_client
from src.llm.llm_utils import extract_info_via_llm, get_groq_client, call_llm_on_prompt
from src.search.search_milvus import search_exact_cve_id, search_vector_embedding


class CVEQueryState(TypedDict):
    query: str
    cve_ids: List[str]
    intent: Optional[Literal["remediation", "summary", "general"]]
    final_results: List[str]


def parse_query(state: CVEQueryState) -> CVEQueryState:
    groq_client = get_groq_client()
    parsed = extract_info_via_llm(query=state["query"], llm_client=groq_client)
    cve_ids = parsed["cve_id"]
    if isinstance(cve_ids, str):
        cve_ids = [cve_ids]
    return {**state, "cve_ids": cve_ids or [], "intent": parsed.get("intent")}


def search_and_generate(state: CVEQueryState) -> CVEQueryState:
    groq_client = get_groq_client()
    milvus_client = get_milvus_client()
    results = []

    print("STATING THE OBVIOUS: ", state)

    cve_ids, intent = state["cve_ids"], state["intent"]
    for cve_id in cve_ids:
        exact_result = search_exact_cve_id(cve_id, intent, milvus_client)
        result_entry = exact_result[0] if exact_result else None

        if not result_entry:
            vector_result = search_vector_embedding(
                state["query"], milvus_client, groq_client
            )
            result_entry = vector_result if vector_result else None

        if not result_entry:
            results.append(f"No data found for {cve_id}")
            continue

        entity = result_entry[0]
        description = entity.get("cve_description", "No description provided.")

        llm_response = call_llm_on_prompt(groq_client, description)
        results.append(f"## {cve_id}\n{llm_response}")

    print("FINAL RESULTS !!!!", results)

    return {**state, "final_results": results}


def build_pipeline():
    state_graph = StateGraph(CVEQueryState)

    state_graph.add_node("parse_query", parse_query)
    state_graph.add_node("search_and_generate", search_and_generate)

    state_graph.set_entry_point("parse_query")
    state_graph.add_edge("parse_query", "search_and_generate")
    state_graph.add_edge("search_and_generate", END)

    return state_graph.compile()


if __name__ == "__main__":
    query = "Summarize CVE-2023-1234 and CVE-2021-34527 with remediation steps"
    graph = build_pipeline()
    result = graph.invoke({"query": query})
