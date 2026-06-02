-- ============================================================
-- Sales Performance Analysis — SQL Queries
-- Compatible with DuckDB, PostgreSQL, and most SQL dialects
-- Usage: duckdb -c ".read sql/analysis.sql" (after install)
-- ============================================================

-- 0. Load CSV into DuckDB (run this first in DuckDB CLI)
-- CREATE TABLE sales AS SELECT * FROM read_csv_auto('data/cleaned/cleaned_data.csv');

-- ============================================================
-- 1. OVERVIEW
-- ============================================================

SELECT
    COUNT(*)                          AS total_orders,
    COUNT(DISTINCT customer_id)       AS unique_customers,
    COUNT(DISTINCT product_id)        AS unique_products,
    ROUND(SUM(sales), 2)              AS total_revenue,
    ROUND(SUM(profit), 2)             AS total_profit,
    ROUND(AVG(discount) * 100, 2)     AS avg_discount_pct
FROM sales;


-- ============================================================
-- 2. REVENUE & PROFIT BY CATEGORY
-- ============================================================

SELECT
    category,
    COUNT(*)                                              AS order_count,
    ROUND(SUM(sales), 2)                                  AS total_revenue,
    ROUND(SUM(profit), 2)                                 AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)  AS profit_margin_pct
FROM sales
GROUP BY category
ORDER BY total_revenue DESC;


-- ============================================================
-- 3. MONTHLY REVENUE TREND
-- ============================================================

SELECT
    DATE_TRUNC('month', order_date)   AS month,
    COUNT(*)                          AS orders,
    ROUND(SUM(sales), 2)              AS revenue,
    ROUND(SUM(profit), 2)             AS profit
FROM sales
GROUP BY 1
ORDER BY 1;


-- ============================================================
-- 4. QUARTERLY PERFORMANCE (SEASONALITY)
-- ============================================================

SELECT
    EXTRACT(YEAR FROM order_date)     AS year,
    EXTRACT(QUARTER FROM order_date)  AS quarter,
    ROUND(SUM(sales), 2)              AS quarterly_revenue,
    ROUND(SUM(profit), 2)             AS quarterly_profit
FROM sales
GROUP BY 1, 2
ORDER BY 1, 2;


-- ============================================================
-- 5. TOP 10 PRODUCTS BY REVENUE
-- ============================================================

SELECT
    product_name,
    COUNT(*)                AS times_ordered,
    ROUND(SUM(sales), 2)    AS total_revenue,
    ROUND(SUM(profit), 2)   AS total_profit
FROM sales
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================
-- 6. REGIONAL PERFORMANCE
-- ============================================================

SELECT
    region,
    state,
    COUNT(DISTINCT customer_id)                           AS customers,
    ROUND(SUM(sales), 2)                                  AS revenue,
    ROUND(SUM(profit), 2)                                 AS profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)  AS margin_pct
FROM sales
GROUP BY region, state
ORDER BY revenue DESC;


-- ============================================================
-- 7. DISCOUNT IMPACT ANALYSIS
-- ============================================================

SELECT
    CASE
        WHEN discount = 0            THEN '0% — No discount'
        WHEN discount <= 0.10        THEN '1–10%'
        WHEN discount <= 0.20        THEN '11–20%'
        WHEN discount <= 0.30        THEN '21–30%'
        ELSE '30%+ (High risk)'
    END AS discount_bucket,
    COUNT(*)                                              AS orders,
    ROUND(AVG(sales), 2)                                  AS avg_order_value,
    ROUND(SUM(profit), 2)                                 AS total_profit,
    ROUND(SUM(profit) / NULLIF(SUM(sales), 0) * 100, 2)  AS margin_pct
FROM sales
GROUP BY 1
ORDER BY 2;


-- ============================================================
-- 8. CUSTOMER LIFETIME VALUE — TOP 10
-- ============================================================

SELECT
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id)      AS total_orders,
    ROUND(SUM(sales), 2)          AS lifetime_value,
    ROUND(AVG(sales), 2)          AS avg_order_value
FROM sales
GROUP BY customer_id, customer_name, segment
ORDER BY lifetime_value DESC
LIMIT 10;


-- ============================================================
-- 9. SHIPPING MODE ANALYSIS
-- ============================================================

SELECT
    ship_mode,
    COUNT(*)                AS shipments,
    ROUND(SUM(sales), 2)    AS revenue,
    ROUND(AVG(
        DATEDIFF('day', order_date, ship_date)
    ), 1)                   AS avg_days_to_ship
FROM sales
GROUP BY ship_mode
ORDER BY revenue DESC;


-- ============================================================
-- 10. YEAR-OVER-YEAR GROWTH (window function)
-- ============================================================

WITH yearly AS (
    SELECT
        EXTRACT(YEAR FROM order_date)  AS year,
        ROUND(SUM(sales), 2)           AS revenue
    FROM sales
    GROUP BY 1
)
SELECT
    year,
    revenue,
    LAG(revenue) OVER (ORDER BY year)  AS prev_year_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year))
        / NULLIF(LAG(revenue) OVER (ORDER BY year), 0) * 100,
    2)                                 AS yoy_growth_pct
FROM yearly
ORDER BY year;
