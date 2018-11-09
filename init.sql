CREATE DATABASE IF NOT EXISTS collect;
ALTER DATABASE collect CHARACTER SET 'utf8mb4' COLLATE 'utf8mb4_unicode_ci';
USE collect;
CREATE TABLE IF NOT EXISTS data(
  order_id TEXT,
  order_status TEXT,
  order_products_value DECIMAL(10, 2),
  order_freight_value DECIMAL(10, 2),
  order_items_qty DECIMAL(10, 2),
  order_sellers_qty DECIMAL(10, 2),
  order_purchase_timestamp TEXT,
  order_aproved_at TEXT(1000),
  order_estimated_delivery_date TEXT(1000),
  order_delivered_customer_date TEXT(1000),
  customer_id TEXT(1000),
  customer_city TEXT(1000),
  customer_state TEXT(1000),
  customer_zip_code_prefix DECIMAL(10, 2),
  product_category_name TEXT(1000),
  product_name_lenght DECIMAL(10, 2),
  product_description_lenght DECIMAL(10, 2),
  product_photos_qty DECIMAL(10, 2),
  product_id TEXT(1000),
  review_id TEXT(1000),
  review_score DECIMAL(10, 2),
  review_creation_date TEXT(1000),
  review_answer_timestamp TEXT(1000)
) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS team(
  Tname TEXT,
  Description TEXT,
  Managers TEXT,
  Members TEXT
);