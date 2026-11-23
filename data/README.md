# Data

## Source
Olist Brazilian E-Commerce Public Dataset
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

**License:** CC BY-NC-SA 4.0 (verify on the Kaggle page). Used here for academic purposes with attribution to Olist.

## Files (9)
| File | Rows |
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

## Where the data lives
- **Full files:** NOT in this repository. Download them from Kaggle, or read them from the project's Bronze layer (`bronze/olist/`, see `docs/data/data_contract.md`, section 6).
- **`sample/`:** the first 100 rows of each file, for quick local testing only. Do not use it for analysis or reconciliation.

## Related documents
- `docs/data/data_dictionary.md`
- `docs/data/source_schema.md`
- `docs/data/data_profiling_report.md`
- `docs/data/data_contract.md`