import time

import src.db_components.milvus as milvus
import src.utils.constants as consts
from src.db_components.insert_data import insert_data_into_db
from src.preprocess.enrich_and_prepare_data import process_all_cves_in_batches

try:
    client = milvus.get_milvus_client()
except Exception as e:
    print(f"Error while creating a Milvus Client: {e}")


def safe_insert(client, chunk, retries=3):
    for attempt in range(1, retries + 1):
        try:
            insert_data_into_db(client, chunk)
            return
        except Exception as e:
            print(f"❌ Attempt {attempt} failed: {e}")
            time.sleep(2 * attempt)
    print(f"❌ Failed to insert chunk after {retries} retries.")


def main():
    for year in range(2014, 2025):
        print(f"\n🔍 Processing CVEs for year: {year}")
        file_path = consts.DATA_DIR / f"nvdcve-1.1-{year}.json"
        list_of_records = process_all_cves_in_batches(
            file_path=file_path, batch_size=consts.SENTENCE_ENCODER_BATCH_SIZE
        )

        if not list_of_records:
            print(f"⚠️ No records found for {year}, skipping...")
            continue

        chunk_size = 500
        total = len(list_of_records)

        for i in range(0, total, chunk_size):
            chunk = list_of_records[i : i + chunk_size]
            print(
                f"📦 Inserting {len(chunk)} records from year {year} (chunk {i // chunk_size + 1})"
            )
            safe_insert(client, chunk)


if __name__ == "__main__":
    main()
