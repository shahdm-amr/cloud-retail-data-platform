"""Validate raw Olist files in Bronze and write an ingestion log.

Usage:
  Local : python validate_ingestion.py --mode local --path C:\\Users\\HI-55\\olist_raw
  Cloud : set the AZURE_SAS env variable first, then
          python validate_ingestion.py --mode cloud
"""
import argparse, io, json, os
import datetime as dt
import pandas as pd

EXPECTED = {
    "olist_customers_dataset.csv": 99441,
    "olist_geolocation_dataset.csv": 1000163,
    "olist_order_items_dataset.csv": 112650,
    "olist_order_payments_dataset.csv": 103886,
    "olist_order_reviews_dataset.csv": 99224,
    "olist_orders_dataset.csv": 99441,
    "olist_products_dataset.csv": 32951,
    "olist_sellers_dataset.csv": 3095,
    "product_category_name_translation.csv": 71,
}

ap = argparse.ArgumentParser()
ap.add_argument("--mode", choices=["local", "cloud"], default="local")
ap.add_argument("--path", help="local folder that holds the CSV files")
args = ap.parse_args()

if args.mode == "cloud":
    from azure.storage.blob import ContainerClient
    sas = os.environ["AZURE_SAS"].lstrip("?")
    cc = ContainerClient("https://euidatapipe01.blob.core.windows.net",
                         "ingestion", credential=sas)

def load(name):
    if args.mode == "local":
        return pd.read_csv(os.path.join(args.path, name))
    data = cc.get_blob_client(f"bronze/olist/{name}").download_blob().readall()
    return pd.read_csv(io.BytesIO(data))

now = dt.datetime.now(dt.timezone.utc)
run_id = now.strftime("%Y%m%dT%H%M%SZ")
log = []

for name, expected in EXPECTED.items():
    try:
        rows = len(load(name))
        status = "SUCCESS" if rows == expected else "MISMATCH"
    except Exception as e:
        rows, status = None, f"FAILED: {type(e).__name__}"
    log.append({
        "run_id": run_id,
        "file": name,
        "source": "Kaggle - Olist Brazilian E-Commerce",
        "mode": args.mode,
        "expected_rows": expected,
        "actual_rows": rows,
        "status": status,
        "checked_at_utc": now.isoformat(),
    })
    print(f"{name:45} {rows!s:>10}  {status}")

out_dir = os.path.dirname(os.path.abspath(__file__))
out_file = os.path.join(out_dir, f"ingestion_log_{run_id}.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(log, f, indent=2)
print("log saved:", out_file)