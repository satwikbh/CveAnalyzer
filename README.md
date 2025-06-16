# 🛡️ CVE Analyzer & Remediation Explorer (2014–2024)

## 📌 Overview

This project ingests top CVEs from the past decade (2014–2024), enriches them with project metadata, and uses LLMs to generate detailed explanations, affected systems, potential exploit paths, and suggested remediation.

🔎 Perfect for security audits, threat modeling, or automated remediation suggestion systems.

---

## 🎯 Project Scope

This project aims to build an intelligent, end-to-end pipeline for enriching and querying Common Vulnerabilities and Exposures (CVEs) using hybrid search, LLMs, and a modern UI. It serves as a centralized assistant for summarizing vulnerabilities, identifying remediation strategies, and supporting security decisions.

✅ **Key Objectives**
- **Ingest & Index** vulnerability data from NVD datasets (2014–2024).
- **Store & Search** CVEs using:
  - Exact CVE ID match (symbolic search).
  - Semantic similarity via vector embeddings (hybrid search).
- **Enhance & Enrich** results with:
  - LLM-powered summarization and remediation strategies.
  - Contextual prompts (root cause, risk, engineering ticket, etc.).
- **Multi-CVE Support** to handle complex queries involving multiple vulnerabilities.
- **LangGraph Orchestration** to control flow and modularity of processing steps.
- **Streamlit Frontend** for querying CVEs and viewing rich, structured insights.
- **LangFuse Integration** for observability and telemetry of the LLM pipeline.

---

## 🧠 Tech Stack

| Category                 | Technology                                   | Purpose                                                                     |
| ------------------------ | -------------------------------------------- | --------------------------------------------------------------------------- |
| **Programming Language** | `Python 3.10+`                               | Main development language                                                   |
| **Vector DB**            | `Milvus`                                     | Hybrid search (exact + semantic) for CVEs                                   |
| **UI Framework**         | `Streamlit`                                  | Lightweight web interface for interacting with the pipeline                 |
| **LLM Orchestration**    | `LangGraph`                                  | Declarative, modular graph-based pipeline orchestration                     |
| **Embedding Model**      | `sentence-transformers` (`BAAI/bge-base-en-v1.5`) | Embedding generator for semantic search                                     |
| **LLM API**              | `Groq API (LLaMA3)`                          | Fast and accurate summarization, intent parsing, and remediation generation |
| **Observability**        | `LangFuse`                                   | LLM pipeline tracing, error monitoring, and latency analysis                |


---

## 📂 Project Structure

    CVE-Analyzer/
    ├── .env
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    ├── requirements.txt
    ├── src/                             # All core logic lives here
    │   ├── __init__.py
    │   ├── db_components/               # Milvus DB utilities
    │   │   ├── __init__.py
    │   │   ├── clear_collection.py
    │   │   ├── create_schema.py
    │   │   ├── insert_data.py
    │   │   └── milvus.py
    │   ├── embed_insert/               # Embedding & Insertion Logic
    │   │   ├── __init__.py
    │   │   └── data_loader.py
    │   ├── ingest/                      # Ingest raw data (e.g., arXiv, CVEs)
    │   │   ├── __init__.py
    │   │   └── arxiv_downloader.py
    │   ├── preprocess/                 # Enrichment and pre-insert pipeline
    │   │   ├── __init__.py
    │   │   └── enrich_and_prepare_data.py
    │   ├── llm/                         # LLM integration and prompts
    │   │   ├── __init__.py
    │   │   ├── llm_utils.py
    │   │   └── prompt_template.py
    │   ├── search/                      # Search logic using Milvus
    │   │   ├── __init__.py
    │   │   └── search_milvus.py
    │   ├── monitoring/                  # Observability (e.g., Langfuse)
    │   │   ├── __init__.py
    │   │   └── langfuse.py
    │   ├── ui/                          # Frontend interface
    │   │   ├── __init__.py
    │   │   └── streamlit_app.py
    │   ├── utils/                       # Common constants and tools
    │   │   ├── __init__.py
    │   │   └── constants.py
    │   └── pipeline.py                  # LangGraph pipeline (multi-CVE support)


---

## 🚀 Getting Started


### 1. Clone and set up environment

```bash
git clone https://github.com/yourhandle/cve-analyzer.git
cd cve-analyzer
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Download and preprocess CVE data

```bash
python data/download_cve_data.py --years 2018 2019 2020 2021 2022 2023
python data/preprocess.py
```

### 3. Enrich CVEs and generate embeddings

```bash
python src/enrich_cves.py
python src/embed_and_store.py
```

### 4. Run Streamlit UI

```bash
streamlit run streamlit_app.py || python -m streamlit run src/ui/streamlit_app.py
```

## 🧪 Evaluation with LangFuse

- Monitor prompt quality across CVEs
- Track hallucinations, inconsistency
- Compare prompt versions (e.g. few-shot vs zero-shot)

**LangFuse Dashboard:** 
- [https://cloud.langfuse.com/](https://cloud.langfuse.com/)
- [http://localhost:3000/project/<PROJECT_ID>](http://localhost:3000/project/cmby4u9t30006o807hff5wkjx)

## 🖼️ Streamlit UI Features

- 🔍 Search CVEs by keyword, CVE ID, or vendor
- 🧠 View LLM-generated summaries and fix suggestions
- ⚙️ Filter by year, severity, exploitability score
- 📤 Export detailed reports (PDF or JSON)

## ✨ Example Output
### CVE-2022-1234

- Summary: Buffer overflow in `libxyz.so` in versions <1.2.4
- Impact: Privilege escalation on Debian 10
- Fix: Upgrade `libxyz` to >=1.2.5, patch vulnerable path
- Future hardening: Use stack canaries, fuzz input sanitizer

## 🧠 Why This Project Matters

- 🛡️ Bridges AI + cybersecurity using LLMs
- 🔄 Automates vulnerability triage, reporting, and patching strategy
- 📊 Real-world application across SecOps, DevSecOps, MLOps, and Red Team workflows

## 📫 Contact

**[Your Name]**
🔗 [LinkedIn](https://linkedin.com/in/satwikbh)
🐙 [GitHub](https://github.com/satwikbh)

---

> "Understand a decade of vulnerabilities. Fix them in minutes. Explain them with LLMs."
