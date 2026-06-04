-- ============================================================
-- E-Commerce Operations Analytics — SQL Analysis
-- Dataset: Olist Brazilian E-Commerce (Kaggle)
-- Tool: DuckDB (run: duckdb ecommerce.db)
-- ============================================================

-- Load tables (run once in DuckDB CLI)
-- CREATE TABLE orders      AS SELECT * FROM read_csv_auto('data/cleaned/orders.csv');
-- CREATE TABLE master      AS SELECT * FROM read_csv_auto('data/cleaned/master.csv');
-- CREATE TABLE products    AS SELECT * FROM read_csv_auto('data/cleaned/products.csv');
-- CREATE TABLE sellers     AS SELECT * FROM read_csv_auto('data/cleaned/sellers.csv');
-- CREATE TABLE reviews     AS SELECT * FROM read_csv_auto('data/cleaned/reviews.csv');
-- CREATE TABLE payments    AS SELECT * FROM read_csv_auto('data/cleaned/payments.csv');
-- CREATE TABLE customers   AS SELECT * FROM read_csv_auto('data/cleaned/customers.csv');


-- ============================================================
-- 1. EXECUTIVE SUMMARY KPIs
-- ============================================================
SELECT
    COUNT(DISTINCT order_id)                                      AS total_orders,
    COUNT(DISTINCT customer_unique_id)                            AS unique_customers,
    COUNT(DISTINCT seller_id)                                     AS total_sellers,
    ROUND(SUM(total_revenue), 2)                                  AS gross_revenue,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value,
    ROUND(AVG(review_score), 2)                                   AS avg_review_score,
    ROUND(AVG(delivery_days_actual), 1)                           AS avg_delivery_days,
    ROUND(AVG(on_time_delivery) * 100, 2)                         AS on_time_delivery_pct
FROM master
WHERE order_status = 'delivered';


-- ============================================================
-- 2. MONTHLY REVENUE & ORDER TREND
-- ============================================================
SELECT
    DATE_TRUNC('month', order_purchase_timestamp::TIMESTAMP)      AS month,
    COUNT(DISTINCT order_id)                                      AS total_orders,
    ROUND(SUM(total_revenue), 2)                                  AS monthly_revenue,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value,
    ROUND(AVG(review_score), 2)                                   AS avg_review
FROM master
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY 1;


-- ============================================================
-- 3. YEAR-OVER-YEAR GROWTH
-- ============================================================
WITH yearly AS (
    SELECT
        purchase_year,
        COUNT(DISTINCT order_id)    AS orders,
        ROUND(SUM(total_revenue),2) AS revenue
    FROM master
    WHERE order_status = 'delivered'
    GROUP BY 1
)
SELECT
    purchase_year,
    orders,
    revenue,
    LAG(revenue) OVER (ORDER BY purchase_year)                    AS prev_year_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY purchase_year))
        / NULLIF(LAG(revenue) OVER (ORDER BY purchase_year), 0) * 100
    , 2)                                                          AS yoy_growth_pct
FROM yearly
ORDER BY 1;


-- ============================================================
-- 4. REVENUE BY PRODUCT CATEGORY (TOP 20)
-- ============================================================
SELECT
    category,
    COUNT(DISTINCT order_id)                                      AS orders,
    ROUND(SUM(total_revenue), 2)                                  AS revenue,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value,
    ROUND(AVG(review_score), 2)                                   AS avg_review,
    ROUND(AVG(delivery_days_actual), 1)                           AS avg_delivery_days
FROM master
WHERE order_status = 'delivered'
  AND category IS NOT NULL
GROUP BY 1
ORDER BY revenue DESC
LIMIT 20;


-- ============================================================
-- 5. GEOGRAPHIC PERFORMANCE BY STATE
-- ============================================================
SELECT
    customer_state                                                AS state,
    COUNT(DISTINCT order_id)                                      AS orders,
    COUNT(DISTINCT customer_unique_id)                            AS customers,
    ROUND(SUM(total_revenue), 2)                                  AS revenue,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value,
    ROUND(AVG(delivery_days_actual), 1)                           AS avg_delivery_days,
    ROUND(AVG(on_time_delivery) * 100, 2)                         AS on_time_pct,
    ROUND(AVG(review_score), 2)                                   AS avg_review
FROM master
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY revenue DESC;


-- ============================================================
-- 6. DELIVERY PERFORMANCE ANALYSIS
-- ============================================================
SELECT
    CASE
        WHEN delivery_days_actual <= 7   THEN '1–7 days (Fast)'
        WHEN delivery_days_actual <= 14  THEN '8–14 days (Normal)'
        WHEN delivery_days_actual <= 21  THEN '15–21 days (Slow)'
        WHEN delivery_days_actual <= 30  THEN '22–30 days (Very Slow)'
        ELSE '30+ days (Critical)'
    END                                                           AS delivery_bucket,
    COUNT(*)                                                      AS orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)           AS pct_of_orders,
    ROUND(AVG(review_score), 2)                                   AS avg_review_score,
    ROUND(AVG(on_time_delivery) * 100, 2)                         AS on_time_pct
FROM master
WHERE order_status = 'delivered'
  AND delivery_days_actual IS NOT NULL
GROUP BY 1
ORDER BY MIN(delivery_days_actual);


-- ============================================================
-- 7. LATE DELIVERY IMPACT ON REVIEW SCORES
-- ============================================================
SELECT
    on_time_delivery,
    CASE WHEN on_time_delivery = 1 THEN 'On Time' ELSE 'Late' END AS delivery_status,
    COUNT(*)                                                      AS orders,
    ROUND(AVG(review_score), 3)                                   AS avg_review,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value
FROM master
WHERE order_status = 'delivered'
  AND on_time_delivery IS NOT NULL
GROUP BY 1, 2
ORDER BY 1 DESC;


-- ============================================================
-- 8. TOP 20 SELLERS BY REVENUE
-- ============================================================
SELECT
    seller_id,
    seller_city,
    seller_state,
    COUNT(DISTINCT order_id)                                      AS total_orders,
    ROUND(SUM(total_revenue), 2)                                  AS total_revenue,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value,
    ROUND(AVG(review_score), 2)                                   AS avg_review,
    ROUND(AVG(on_time_delivery) * 100, 2)                         AS on_time_pct
FROM master
WHERE order_status = 'delivered'
GROUP BY 1, 2, 3
ORDER BY total_revenue DESC
LIMIT 20;


-- ============================================================
-- 9. CUSTOMER SEGMENTATION BY PURCHASE FREQUENCY
-- ============================================================
WITH customer_orders AS (
    SELECT
        customer_unique_id,
        COUNT(DISTINCT order_id)    AS order_count,
        ROUND(SUM(total_revenue),2) AS lifetime_value,
        ROUND(AVG(review_score),2)  AS avg_review,
        MIN(order_purchase_timestamp::TIMESTAMP) AS first_order,
        MAX(order_purchase_timestamp::TIMESTAMP) AS last_order
    FROM master
    WHERE order_status = 'delivered'
    GROUP BY 1
)
SELECT
    CASE
        WHEN order_count = 1  THEN 'One-Time Buyer'
        WHEN order_count <= 3 THEN 'Repeat Buyer'
        ELSE 'Loyal Customer'
    END                                                           AS segment,
    COUNT(*)                                                      AS customers,
    ROUND(AVG(lifetime_value), 2)                                 AS avg_lifetime_value,
    ROUND(AVG(order_count), 1)                                    AS avg_orders,
    ROUND(AVG(avg_review), 2)                                     AS avg_review
FROM customer_orders
GROUP BY 1
ORDER BY avg_lifetime_value DESC;


-- ============================================================
-- 10. PAYMENT TYPE ANALYSIS
-- ============================================================
SELECT
    payment_type,
    COUNT(DISTINCT order_id)                                      AS orders,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2)           AS pct_share,
    ROUND(SUM(payment_value), 2)                                  AS total_value,
    ROUND(AVG(payment_value), 2)                                  AS avg_payment,
    ROUND(AVG(payment_installments), 1)                           AS avg_installments
FROM master
WHERE order_status = 'delivered'
GROUP BY 1
ORDER BY orders DESC;


-- ============================================================
-- 11. REVIEW SCORE IMPACT ON BUSINESS
-- ============================================================
SELECT
    review_score,
    COUNT(*)                                                      AS orders,
    ROUND(AVG(total_revenue), 2)                                  AS avg_order_value,
    ROUND(AVG(delivery_days_actual), 1)                           AS avg_delivery_days,
    ROUND(AVG(on_time_delivery) * 100, 2)                         AS on_time_pct
FROM master
WHERE order_status = 'delivered'
  AND review_score IS NOT NULL
GROUP BY 1
ORDER BY 1;


-- ============================================================
-- 12. PEAK HOURS ANALYSIS
-- ============================================================
SELECT
    purchase_hour,
    COUNT(DISTINCT order_id)                                      AS orders,
    ROUND(SUM(total_revenue), 2)                                  AS revenue
FROM master
GROUP BY 1
ORDER BY 1;


-- ============================================================
-- 13. QUARTERLY PERFORMANCE
-- ============================================================
SELECT
    purchase_year                                                 AS year,
    purchase_quarter                                              AS quarter,
    COUNT(DISTINCT order_id)                                      AS orders,
    ROUND(SUM(total_revenue), 2)                                  AS revenue,
    ROUND(AVG(review_score), 2)                                   AS avg_review,
    ROUND(AVG(on_time_delivery)*100, 2)                           AS on_time_pct
FROM master
WHERE order_status = 'delivered'
GROUP BY 1, 2
ORDER BY 1, 2;


-- ============================================================
-- 14. FREIGHT VALUE ANALYSIS
-- ============================================================
SELECT
    category,
    ROUND(AVG(total_freight), 2)                                  AS avg_freight,
    ROUND(AVG(total_price), 2)                                    AS avg_price,
    ROUND(AVG(total_freight) / NULLIF(AVG(total_price),0)*100,2) AS freight_pct_of_price,
    COUNT(DISTINCT order_id)                                      AS orders
FROM master
WHERE order_status = 'delivered'
  AND category IS NOT NULL
GROUP BY 1
ORDER BY freight_pct_of_price DESC
LIMIT 15;


-- ============================================================
-- 15. CANCELLATION RATE BY CATEGORY
-- ============================================================
SELECT
    category,
    COUNT(DISTINCT order_id)                                      AS total_orders,
    SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END)   AS canceled,
    ROUND(
        SUM(CASE WHEN order_status = 'canceled' THEN 1 ELSE 0 END)
        * 100.0 / COUNT(DISTINCT order_id)
    , 2)                                                          AS cancel_rate_pct
FROM master
WHERE category IS NOT NULL
GROUP BY 1
HAVING COUNT(DISTINCT order_id) > 100
ORDER BY cancel_rate_pct DESC
LIMIT 15;
