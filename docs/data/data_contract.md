# Data Contract

## 1. Naming
- All columns: lowercase snake_case.
- Renames in Silver: `product_name_lenght` → `product_name_length`, `product_description_lenght` → `product_description_length`.

## 2. Data types (Silver)
| Type | Columns |
|---|---|
| string | all IDs, status, city, state, payment_type, category names |
| string (5 chars) | all `*_zip_code_prefix` |
| timestamp | all `*_timestamp`, `*_date`, `*_at` columns in orders; `shipping_limit_date` |
| decimal(10,2) | price, freight_value, payment_value |
| int | order_item_id, payment_sequential, payment_installments, product_* counts and measures |

## 3. Keys
customers: customer_id | orders: order_id | order_items: (order_id, order_item_id) | products: product_id | sellers: seller_id | order_payments: (order_id, payment_sequential)

## 4. Decisions
- Store dimension = Sellers (assumption; not real branch data).
- Fact grain: one row per order item (order_id + order_item_id).
- Dim_Customer is built on customer_unique_id.
- Orders without items (775, non-completed statuses) are excluded from Fact_Sales.
- Missing product_category_name → `unknown`.
- Missing translations added manually: pc_gamer → pc_gamer, portateis_cozinha_e_preparadores_de_alimentos → portable_kitchen_food_preparers.
- Net Sales definition (with or without freight_value): to be agreed with Member 5.

## 5. Bronze
Raw files are kept unchanged, with original names and types.

## 6. Bronze location (actual)

Container: `ingestion` on storage account `euidatapipe01` (flat Blob, not ADLS Gen2).
Path pattern: `wasbs://ingestion@euidatapipe01.blob.core.windows.net/bronze/olist/<file>.csv`

All 9 raw files are in one folder, `bronze/olist/`, unchanged:

| Logical group | Files |
|---|---|
| sales | olist_orders_dataset.csv, olist_order_items_dataset.csv, olist_order_payments_dataset.csv |
| products | olist_products_dataset.csv, product_category_name_translation.csv |
| customers | olist_customers_dataset.csv |
| stores (sellers) | olist_sellers_dataset.csv |
| pending agreement | olist_order_reviews_dataset.csv, olist_geolocation_dataset.csv |

Next layers (same container): `silver/`, then `gold/`.
Access tokens are shared privately and must never be committed to GitHub.
Note: if ADLS Gen2 is enabled later, paths change from `wasbs://` to `abfss://`.