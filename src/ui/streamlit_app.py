import os
import sys

import streamlit as st

from src.pipeline import build_pipeline

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

st.set_page_config(page_title="CVE Assistant", layout="wide")
st.title("🛡️ CVE Enrichment Assistant")

query = st.text_area(
    "Enter your query:",
    height=150,
    placeholder="e.g., Summarize CVE-2023-1234 and CVE-2021-34527",
)
if st.button("Submit"):
    with st.spinner("Processing your request..."):
        graph = build_pipeline()
        result = graph.invoke({"query": query})
        final_results = result.get("final_results", [])

    st.markdown("### 🔍 Results")
    for res in final_results:
        st.markdown(res)
