"""
clean_data.py
-------------
Cleans and merges all 9 Olist datasets into a single master analytics table.
Run: python src/clean_data.py

Output files in data/cleaned/:
  - master.csv          → full joined dataset (used for Tableau)
  - orders.csv          → cleaned orders
  - customers.csv       → cleaned customers
  - products.csv        → cleaned products with English names
  - sellers.csv         → cleaned sellers
  - payments.csv        → cleaned payments
  - reviews.csv         → cleaned reviews
  - kpi_summary.csv     → pre-aggregated KPIs for dashboard
"""

import pandas as pd
import numpy as np
from pathlib import Path

RAW = Path("data/raw")
OUT = Path("data/cleaned")
OUT.mkdir(parents=True, exist_ok=True)


# ── Load ───────────────────────────────────────────────────────────────────────

def load():
    print("Loading raw files...")
    data = {}
    data["orders"]      = pd.read_csv(RAW / "olist_orders_dataset.csv")
    data["customers"]   = pd.read_csv(RAW / "olist_customers_dataset.csv")
    data["items"]       = pd.read_csv(RAW / "olist_order_items_dataset.csv")
    data["payments"]    = pd.read_csv(RAW / "olist_order_payments_dataset.csv")
    data["reviews"]     = pd.read_csv(RAW / "olist_order_reviews_dataset.csv")
    data["products"]    = pd.read_csv(RAW / "olist_products_dataset.csv")
    data["sellers"]     = pd.read_csv(RAW / "olist_sellers_dataset.csv")
    data["geo"]         = pd.read_csv(RAW / "olist_geolocation_dataset.csv")
    data["categories"]  = pd.read_csv(RAW / "product_category_name_translation.csv")
    for k, v in data.items():
        print(f"  {k:12s}: {len(v):>7,} rows")
    return data


# ── Clean individual tables ────────────────────────────────────────────────────

def clean_orders(df):
    date_cols = [
        "order_purchase_timestamp", "order_approved_at",
        "order_delivered_carrier_date", "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    df = df.drop_duplicates(subset="order_id")

    # Delivery time in days
    df["delivery_days_actual"] = (
        df["order_delivered_customer_date"] - df["order_purchase_timestamp"]
    ).dt.days

    df["delivery_days_estimated"] = (
        df["order_estimated_delivery_date"] - df["order_purchase_timestamp"]
    ).dt.days

    # On-time flag: 1 = on time, 0 = late
    df["on_time_delivery"] = (
        df["order_delivered_customer_date"] <= df["order_estimated_delivery_date"]
    ).astype("Int64")

    # Time features
    df["purchase_year"]    = df["order_purchase_timestamp"].dt.year
    df["purchase_month"]   = df["order_purchase_timestamp"].dt.month
    df["purchase_quarter"] = df["order_purchase_timestamp"].dt.quarter
    df["purchase_dow"]     = df["order_purchase_timestamp"].dt.day_name()
    df["purchase_hour"]    = df["order_purchase_timestamp"].dt.hour

    return df


def clean_items(df):
    df = df.drop_duplicates()
    # Revenue per item = price + freight
    df["item_revenue"] = df["price"] + df["freight_value"]
    return df


def clean_products(df, categories):
    df = df.drop_duplicates(subset="product_id")
    df = df.merge(categories, on="product_category_name", how="left")
    df["product_category_name_english"] = df["product_category_name_english"].fillna("Other")
    # Fill numeric nulls with median
    for col in ["product_weight_g", "product_length_cm", "product_height_cm", "product_width_cm"]:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
    return df


def clean_reviews(df):
    df = df.drop_duplicates(subset="review_id")
    df["review_creation_date"] = pd.to_datetime(df["review_creation_date"], errors="coerce")
    # Sentiment bucket
    df["sentiment"] = pd.cut(
        df["review_score"],
        bins=[0, 2, 3, 5],
        labels=["Negative", "Neutral", "Positive"]
    )
    return df


def clean_payments(df):
    df = df.drop_duplicates()
    return df


def clean_customers(df):
    df = df.drop_duplicates(subset="customer_id")
    return df


def clean_sellers(df):
    df = df.drop_duplicates(subset="seller_id")
    return df


# ── Build master table ─────────────────────────────────────────────────────────

def build_master(data):
    print("\nBuilding master table...")

    orders    = data["orders"]
    items     = data["items"]
    payments  = data["payments"]
    reviews   = data["reviews"]
    customers = data["customers"]
    products  = data["products"]
    sellers   = data["sellers"]

    # Aggregate items to order level
    items_agg = items.groupby("order_id").agg(
        item_count    = ("order_item_id", "count"),
        total_price   = ("price", "sum"),
        total_freight = ("freight_value", "sum"),
        total_revenue = ("item_revenue", "sum"),
        seller_id     = ("seller_id", "first"),
        product_id    = ("product_id", "first"),
    ).reset_index()

    # Aggregate payments to order level
    pay_agg = payments.groupby("order_id").agg(
        payment_value       = ("payment_value", "sum"),
        payment_installments = ("payment_installments", "max"),
        payment_type        = ("payment_type", "first"),
    ).reset_index()

    # Best review per order
    rev_agg = reviews.sort_values("review_score", ascending=False).drop_duplicates("order_id")[
        ["order_id", "review_score", "sentiment"]
    ]

    # Join everything
    master = (
        orders
        .merge(items_agg,  on="order_id",   how="left")
        .merge(pay_agg,    on="order_id",   how="left")
        .merge(rev_agg,    on="order_id",   how="left")
        .merge(customers,  on="customer_id", how="left")
        .merge(products,   on="product_id", how="left")
        .merge(sellers,    on="seller_id",  how="left")
    )

    # Rename for clarity
    master = master.rename(columns={
        "customer_city":  "customer_city",
        "customer_state": "customer_state",
        "seller_city":    "seller_city",
        "seller_state":   "seller_state",
        "product_category_name_english": "category",
    })

    print(f"  Master shape: {master.shape}")
    return master


# ── KPI Summary ────────────────────────────────────────────────────────────────

def build_kpi_summary(master):
    delivered = master[master["order_status"] == "delivered"]

    kpis = {
        "total_orders":           len(master),
        "delivered_orders":       len(delivered),
        "total_revenue":          round(delivered["total_revenue"].sum(), 2),
        "avg_order_value":        round(delivered["total_revenue"].mean(), 2),
        "avg_review_score":       round(delivered["review_score"].mean(), 2),
        "avg_delivery_days":      round(delivered["delivery_days_actual"].mean(), 1),
        "on_time_delivery_rate":  round(delivered["on_time_delivery"].mean() * 100, 2),
        "total_customers":        master["customer_unique_id"].nunique(),
        "total_sellers":          master["seller_id"].nunique(),
        "total_categories":       master["category"].nunique(),
    }

    kpi_df = pd.DataFrame(list(kpis.items()), columns=["kpi", "value"])
    return kpi_df


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    data = load()

    print("\nCleaning tables...")
    data["orders"]    = clean_orders(data["orders"])
    data["items"]     = clean_items(data["items"])
    data["products"]  = clean_products(data["products"], data["categories"])
    data["reviews"]   = clean_reviews(data["reviews"])
    data["payments"]  = clean_payments(data["payments"])
    data["customers"] = clean_customers(data["customers"])
    data["sellers"]   = clean_sellers(data["sellers"])

    # Save individual clean tables
    tables = ["orders", "customers", "products", "sellers", "payments", "reviews"]
    for t in tables:
        path = OUT / f"{t}.csv"
        data[t].to_csv(path, index=False)
        print(f"  ✓ Saved {path}")

    # Build and save master
    master = build_master(data)
    master.to_csv(OUT / "master.csv", index=False)
    print(f"  ✓ Saved data/cleaned/master.csv")

    # Build and save KPIs
    kpis = build_kpi_summary(master)
    kpis.to_csv(OUT / "kpi_summary.csv", index=False)
    print(f"  ✓ Saved data/cleaned/kpi_summary.csv")

    print("\n" + "=" * 50)
    print("CLEANING COMPLETE")
    print("=" * 50)
    print(f"  Total orders  : {len(master):,}")
    print(f"  Total revenue : ${master['total_revenue'].sum():,.0f}")
    print(f"  Avg review    : {master['review_score'].mean():.2f} / 5")
    print(f"  On-time rate  : {master['on_time_delivery'].mean()*100:.1f}%")
    print(f"\n  → Open Tableau and connect to: data/cleaned/master.csv")


if __name__ == "__main__":
    main()
