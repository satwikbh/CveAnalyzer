import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor

import requests

from src.utils.constants import DATA_DIR, ARXIV_BASE_URL

DATA_DIR.mkdir(parents=True, exist_ok=True)


def download_and_extract(year):
    gz_path = DATA_DIR / f"nvdcve-1.1-{year}.json.gz"
    json_path = gz_path.with_suffix("")

    if json_path.exists():
        return f"[✓] {year} already exists."

    try:
        url = f"{ARXIV_BASE_URL}/nvdcve-1.1-{year}.json.gz"
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(gz_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        with gzip.open(gz_path, "rb") as f_in, open(json_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
        return f"[✓] Downloaded + Extracted {year}"
    except Exception as e:
        return f"[!] Failed {year}: {e}"


if __name__ == "__main__":
    years = list(range(2014, 2025))
    with ThreadPoolExecutor(max_workers=6) as executor:
        results = executor.map(download_and_extract, years)
        for res in results:
            print(res)
