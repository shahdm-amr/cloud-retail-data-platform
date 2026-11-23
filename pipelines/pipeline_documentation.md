# Ingestion Documentation

**Owner:** Member 2, Data Sources & Ingestion
**Branch:** `feature/ingestion`

## 1. Purpose

This document describes how the raw Olist data reaches the Bronze layer and how we verify that it arrived complete and unchanged. Bronze keeps the data exactly as received from the source: no cleaning, no type changes, no renaming.

## 2. Data source

| Item | Value |
|---|---|
| Dataset | Olist Brazilian E-Commerce Public Dataset |
| Link | https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce |
| License | CC BY-NC-SA 4.0 (verify on the Kaggle page) |
| Format | 9 CSV files |
| Details | `data/README.md`, `docs/data/data_contract.md` |

## 3. Bronze location

- Storage account: `euidatapipe01` (flat Blob storage, ADLS Gen2 not enabled)
- Container: `ingestion`
- Folder: `bronze/olist/`
- Path pattern: `wasbs://ingestion@euidatapipe01.blob.core.windows.net/bronze/olist/<file>.csv`
- Next layers (same container): `silver/`, then `gold/`

Access is through a SAS token that is shared privately within the team. **The token must never be committed to GitHub**, written in notebooks, or placed in any file in this repository.

## 4. Files and expected row counts

| File | Expected rows |
|---|---|
| olist_customers_dataset.csv | 99,441 |
| olist_geolocation_dataset.csv | 1,000,163 |
| olist_order_items_dataset.csv | 112,650 |
| olist_order_payments_dataset.csv | 103,886 |
| olist_order_reviews_dataset.csv | 99,224 |
| olist_orders_dataset.csv | 99,441 |
| olist_products_dataset.csv | 32,951 |
| olist_sellers_dataset.csv | 3,095 |
| product_category_name_translation.csv | 71 |

Expected counts come from the profiling of the original Kaggle files (`docs/data/data_profiling_report.md`).

## 5. How ingestion was done

The 9 files were uploaded to `bronze/olist/` by the infrastructure side of the team, from the original Kaggle download, without modification. Member 2 did not upload them directly. The upload is verified by the validation script below.

## 6. Validation script

**File:** `pipelines/ingestion/validate_ingestion.py`

For each of the 9 files the script reads the file, counts the rows, compares the count with the expected value, and writes a JSON log.

**Run locally** (on the original CSV files):

```powershell
python pipelines\ingestion\validate_ingestion.py --mode local --path <folder with the CSV files>
```

**Run against Bronze on Azure:**

```powershell
pip install azure-storage-blob
$env:AZURE_SAS = "<token, shared privately>"
python pipelines\ingestion\validate_ingestion.py --mode cloud
```

**Statuses**

| Status | Meaning |
|---|---|
| SUCCESS | Row count equals the expected count |
| MISMATCH | Row count differs from the expected count |
| FAILED | The file could not be read (missing file, permissions, connection) |

## 7. Ingestion log

Each run writes `pipelines/ingestion/ingestion_log_<run_id>.json`, with one record per file:

| Field | Description |
|---|---|
| run_id | UTC timestamp of the run |
| file | File name |
| source | Data source |
| mode | `local` or `cloud` |
| expected_rows | Expected row count |
| actual_rows | Row count found |
| status | SUCCESS, MISMATCH or FAILED |
| checked_at_utc | Time of the check |

## 8. Latest results

| Run | Mode | Files | Result |
|---|---|---|---|
| 20261123T151436Z | local | 9 | 9 SUCCESS |
| [run id] | cloud (Bronze) | [ ] | [ ] |

The local run confirms that the original files match the profiling numbers. The cloud run confirms that the files in Bronze match the original files. Evidence: the log files in `pipelines/ingestion/`.

## 9. Deviations from the original plan

| Plan | Actual | Reason / status |
|---|---|---|
| Synapse Pipeline with Copy Data activity | Python validation script | No Synapse workspace available to Member 2 at this time. Pending decision with Member 1 and Member 3. |
| ADLS Gen2 with `01-raw/sales/`, `products/`, ... | Blob storage with `bronze/olist/` (one folder) | Storage account is flat Blob. Folder mapping is in the Data Contract, section 6. |
| `abfss://` paths | `wasbs://` paths | Follows from using Blob storage. Paths change if ADLS Gen2 is enabled later. |
| Ingestion metadata in `05-audit/ingestion/` | Log files in `pipelines/ingestion/` | Audit folder not agreed yet. To be moved to the storage account once agreed. |

## 10. Known limitations

- The script verifies row counts only. It does not compare file contents or checksums.
- Re-running the script is safe: it only reads data and writes a new log file, and never modifies Bronze.
- `order_reviews` contains multi-line comments. The script reads it with pandas, which handles them correctly. When reading it in Spark, use `multiLine=True`.

## 11. Open items

- [ ] Run the script in `cloud` mode and add the result to section 8.
- [ ] Decision on Synapse: if it becomes available, add a Copy Data pipeline (JSON in `pipelines/ingestion/`) with the same logging fields.
- [ ] Agree on the audit folder name in the storage account.