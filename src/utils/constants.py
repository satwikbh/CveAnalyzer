from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

ARXIV_BASE_URL = "https://nvd.nist.gov/feeds/json/cve/1.1"
DATA_DIR = PROJECT_ROOT / "data/raw"
LANCE_DB_DIR = PROJECT_ROOT / "data/lancedb"
MILVUS_COLLECTION_NAME = "CVEs"

SENTENCE_ENCODER_BATCH_SIZE = 64
