import os
import requests
import pandas as pd
from datetime import datetime
import pyarrow as pa
import pyarrow.parquet as pq
import boto3

# === CONFIG ===
BUCKET = "openfood-bronze"
DATA_DIR = "data/bronze"
PAGE_SIZE = 1000
MAX_PAGES = 5

today_str = datetime.today().strftime("%Y-%m-%d")
output_path = f"{DATA_DIR}/openfood_{today_str}.parquet"

# === COLECT DATA FROM API ===
def fetch_openfood_data():
    all_products = []

    for page in range(1, MAX_PAGES + 1):
        print(f"Colecting page {page}...")
        url = "https://world.openfoodfacts.org/cgi/search.pl"
        params = {
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": PAGE_SIZE,
            "page": page,
        }

        res = requests.get(url, params=params)
        res.raise_for_status()
        data = res.json()
        products = data.get("products", [])
        all_products.extend(products)

    return all_products

# === SAVE AS PARQUET ===
def save_parquet(data, path):
    df = pd.json_normalize(data)

    # Columns to string
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str)

    table = pa.Table.from_pandas(df)
    pq.write_table(table, path)
    print(f"File saved in: {path}")

# === ENVIAR PARA S3 ===
def upload_to_s3(path, bucket, s3_key):
    s3 = boto3.client("s3")
    s3.upload_file(path, bucket, s3_key)
    print(f"Sent to S3: s3://{bucket}/{s3_key}")

# === EXECUTION ===
if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)

    data = fetch_openfood_data()
    save_parquet(data, output_path)

    s3_key = f"raw/{today_str}/openfood.parquet"
    upload_to_s3(output_path, BUCKET, s3_key)