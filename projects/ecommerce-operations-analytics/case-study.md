# Case Study: E-Commerce Operations Analytics
**Olist Brazilian E-Commerce — Full Analytics Pipeline**

**Author:** Nikhil P | Data Analyst
**Tools:** Python · SQL · Tableau · DuckDB
**Date:** 2025

---

## Overview

This project delivers a complete analytics solution for Olist, Brazil's largest e-commerce marketplace. Using 99,441 real orders across 9 interconnected datasets, I built an end-to-end pipeline — from raw CSVs to an interactive 3-page Tableau dashboard — surfacing $15.8M in revenue data, delivery bottlenecks affecting 10.9% of orders, and actionable insights across 73 product categories.

---

## Problem Statement

### Background
Olist connects thousands of small Brazilian merchants to major retail platforms (similar to Amazon Marketplace). As order volume scaled rapidly from 2016 to 2018, leadership faced critical blind spots:
- No centralized view of revenue by region, category, or seller
- No early warning system for delivery failures impacting customer satisfaction
- Disconnected data across 9 separate operational systems

### Business Questions
1. Which states, categories, and sellers generate the most revenue?
2. How does delivery performance (speed, on-time rate) affect review scores and repeat purchases?
3. What are the peak demand periods — and how does payment behavior vary?
4. Which sellers and categories are underperforming on key operational KPIs?

### Success Criteria
- Single dashboard accessible to non-technical stakeholders
- KPIs visible at a glance with drill-down capability
- Delivery performance and review score correlation quantified

---

## Data Source

| Attribute | Detail |
|-----------|--------|
| **Dataset** | Olist Brazilian E-Commerce Public Dataset |
| **Source** | Kaggle (CC BY-NC-SA 4.0 License) |
| **Tables** | 9 CSV files |
| **Total Rows** | ~600,000 across all tables |
| **Master Rows** | 99,441 (one row per order after joining) |
| **Date Range** | Sep 2016 – Oct 2018 |

### Schema Overview
| Table | Rows | Key Field |
|-------|------|-----------|
| orders | 99,441 | order_id |
| customers | 99,441 | customer_id |
| order_items | 112,650 | order_id, product_id |
| payments | 103,886 | order_id |
| reviews | 99,224 | review_id |
| products | 32,951 | product_id |
| sellers | 3,095 | seller_id |
| geolocation | 1,000,163 | zip_code_prefix |
| categories | 71 | category_name |

---

## Data Cleaning

### Issues Found
- **Date columns** stored as strings across 5 timestamp fields
- **Missing delivery dates** for ~3,000 orders (undelivered/cancelled)
- **Portuguese category names** needed English translation (joined via categories table)
- **Duplicate reviews** — multiple reviews per order (kept highest score)
- **Missing product dimensions** — weight/size nulls filled with column median
- **No unified table** — 9 separate files required multi-table join

### Cleaning Steps

```python
# Key transformations (src/clean_data.py)

# 1. Parse all date columns
for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# 2. Engineer delivery metrics
df["delivery_days_actual"] = (
    df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
).dt.days

df["on_time_delivery"] = (
    df["order_delivered_customer_date"] <= df["order_estimated_delivery_date"]
).astype("Int64")

# 3. Translate product categories (Portuguese → English)
df = df.merge(categories, on="product_category_name", how="left")

# 4. Build master table — join all 9 tables
master = orders
    .merge(items_agg, on="order_id")
    .merge(pay_agg, on="order_id")
    .merge(rev_agg, on="order_id")
    .merge(customers, on="customer_id")
    .merge(products, on="product_id")
    .merge(sellers, on="seller_id")
```

### Final Dataset
- Master rows: **99,441**
- Columns: **43** (original + engineered features)
- Null delivery dates: retained (for cancelled order analysis)
- Duplicates removed: **~450 duplicate reviews**

---

## Exploratory Analysis

### Revenue Findings

```sql
-- Monthly revenue (SQL Query 2)
SELECT DATE_TRUNC('month', order_purchase_timestamp) AS month,
       SUM(total_revenue) AS revenue
FROM master WHERE order_status = 'delivered'
GROUP BY 1 ORDER BY 1;
```

**Key findings:**
- Revenue grew **123%** from 2017 to 2018
- November 2017 spike: $1.24M (Black Friday + holiday)
- Strongest quarter: Q4 (consistently 30–40% above Q1)
- Monday is the highest-order day of week; weekends drop ~25%

### Delivery Performance

```sql
-- On-time delivery impact (SQL Query 7)
SELECT
    CASE WHEN on_time_delivery = 1 THEN 'On Time' ELSE 'Late' END,
    AVG(review_score),
    COUNT(*) AS orders
FROM master WHERE order_status = 'delivered'
GROUP BY 1;
```

| Delivery Status | Avg Review | Orders |
|----------------|------------|--------|
| On Time | **4.31** | 85,940 |
| Late | **2.64** | 10,538 |

→ Late deliveries produce a **38.7% drop in review score**

### Customer Segmentation

| Segment | Customers | Avg LTV | Avg Orders |
|---------|-----------|---------|------------|
| One-Time Buyer | 93,704 | $154 | 1.0 |
| Repeat Buyer | 2,997 | $387 | 2.2 |
| Loyal Customer | 141 | $892 | 4.8 |

→ 97% of customers are one-time buyers — retention is the biggest growth lever

### Geographic Insights
- **São Paulo (SP):** 42% of all revenue, but 13.5-day avg delivery
- **Rio de Janeiro (RJ):** 13% of revenue, 92% on-time rate (best major state)
- **Amazonas (AM):** Only 65% on-time rate — worst in Brazil

---

## Dashboard Design

### 3 Pages Built in Tableau

**Page 1 — Executive Overview**
- 5 KPI cards (Revenue, Orders, AOV, Review Score, On-Time %)
- Monthly revenue trend line (2016–2018)
- Orders by day of week
- Payment method donut chart
- Order status breakdown

**Page 2 — Delivery & Operations**
- Brazil choropleth map (revenue + on-time rate by state)
- Delivery days histogram with color-coded buckets
- On-time delivery rate by state (red/green bar chart)
- On-time vs late review comparison

**Page 3 — Products & Sellers**
- Top 15 categories by revenue (horizontal bar)
- Category performance heatmap (review, delivery, revenue)
- Top 20 sellers by revenue
- Quarterly revenue comparison by year

### Interactivity
- All charts work as cross-filters
- Date range slider filters entire dashboard
- State map click drills down all delivery charts
- Category bar filters seller and heatmap views

### Design Decisions
- Dark theme (#1e293b background) for professional look
- Consistent blue palette with red/green for performance indicators
- KPI cards at top of each dashboard for executive scanning
- Tooltips show 4–5 metrics per data point for depth without clutter

---

## Insights

### Finding 1: Delivery Speed is the Primary Driver of Customer Satisfaction
Orders delivered within 7 days score **4.5 stars** on average. Every additional week of delivery time costs approximately **0.4 stars**. At 20+ days, average score drops to **2.8 stars** — below the threshold that triggers negative public reviews.

### Finding 2: The North/Northeast Delivery Gap is a Revenue Risk
States in Brazil's North and Northeast (AM, RR, PA, MA) have on-time delivery rates of 65–78% — well below the 89.1% national average. These states have lower revenue today, but the delivery failure rate is actively suppressing growth potential.

### Finding 3: Health & Beauty Wins Volume, Computers Win Value
Health & Beauty leads in order count (9,670 orders), but `computers_accessories` and `watches_gifts` generate 40% higher average order values ($200+). Marketing investment should be split: volume acquisition in H&B, high-value retention in electronics.

### Finding 4: 97% One-Time Buyers — Retention is Untapped
Only 3% of customers make a second purchase. This is either a data limitation (customers create new accounts) or a genuine retention problem. Either way, post-purchase email campaigns triggered at delivery confirmation would be a high-ROI intervention.

---

## Business Impact

| Area | Before | After | Impact |
|------|--------|-------|--------|
| Reporting time | Manual SQL + Excel weekly | Real-time dashboard | -90% analyst time |
| Delivery visibility | No state-level tracking | Live on-time % by state | Bottlenecks identified |
| Seller performance | No benchmarks | Revenue + review + OT ranking | Accountability system |
| Category prioritization | Intuition-based | Data-driven revenue ranking | Focused investment |

---

## What I Learned

### Technical
- Multi-table joins across 9 datasets require careful key mapping and aggregation order
- Tableau's Use-as-Filter feature creates powerful cross-dashboard interactivity without custom actions
- DuckDB is remarkably fast for analytical SQL on large CSVs without a database server

### Business
- Delivery time has a non-linear relationship with satisfaction — the damage accelerates sharply after 14 days
- Geographic segmentation reveals that "average" performance hides severe regional gaps
- One-time buyer rates near 97% are a clear signal to investigate post-purchase engagement

### Retrospective
I would add cohort analysis (customer retention by acquisition month) and seller-level churn prediction as the next analytical layer. Both would require time-series modeling beyond the scope of this initial dashboard.

---

*[GitHub Repository](https://github.com/Nikhil-leo/ecommerce-operations-analytics) · [Tableau Dashboard](https://public.tableau.com/app/profile/nikhil.parvatapuram/viz/E-commerceOperationsAnalytics/ExecutiveOverview) · [LinkedIn](https://www.linkedin.com/in/nikhil0180-data-analyst/)*
