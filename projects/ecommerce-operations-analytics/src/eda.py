"""
eda.py
------
Generates key EDA charts and saves them to assets/
Run: python src/eda.py

Requires: data/cleaned/master.csv (run clean_data.py first)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from pathlib import Path

MASTER = Path("data/cleaned/master.csv")
ASSETS = Path("assets")
ASSETS.mkdir(exist_ok=True)

sns.set_theme(style="darkgrid", palette="Blues_d")
plt.rcParams.update({"figure.figsize": (12, 5), "axes.titlesize": 14,
                     "axes.titleweight": "bold", "figure.dpi": 150})


def usd(x, _):
    return f"${x:,.0f}"


def load():
    df = pd.read_csv(MASTER, parse_dates=["order_purchase_timestamp"])
    return df[df["order_status"] == "delivered"].copy()


# ── 1. Monthly Revenue Trend ───────────────────────────────────────────────────

def plot_monthly_revenue(df):
    monthly = (
        df.groupby(df["order_purchase_timestamp"].dt.to_period("M"))["total_revenue"]
        .sum().reset_index()
    )
    monthly["order_purchase_timestamp"] = monthly["order_purchase_timestamp"].astype(str)

    fig, ax = plt.subplots()
    ax.fill_between(range(len(monthly)), monthly["total_revenue"], alpha=0.2, color="#3b82f6")
    ax.plot(range(len(monthly)), monthly["total_revenue"], color="#3b82f6", linewidth=2.5)
    ax.set_xticks(range(0, len(monthly), 3))
    ax.set_xticklabels(monthly["order_purchase_timestamp"][::3], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(usd))
    ax.set_title("Monthly Revenue Trend (2016–2018)")
    ax.set_xlabel("")
    plt.tight_layout()
    plt.savefig(ASSETS / "01_monthly_revenue.png")
    plt.close()
    print("  ✓ 01_monthly_revenue.png")


# ── 2. Revenue by Category (Top 15) ───────────────────────────────────────────

def plot_category_revenue(df):
    cat = (
        df.groupby("category")["total_revenue"]
        .sum().sort_values(ascending=True).tail(15)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(cat.index, cat.values, color="#3b82f6", edgecolor="none")
    ax.bar_label(bars, labels=[f"${v:,.0f}" for v in cat.values],
                 padding=4, fontsize=9, color="white")
    ax.set_title("Top 15 Product Categories by Revenue")
    ax.set_xlabel("Total Revenue (BRL)")
    ax.xaxis.set_major_formatter(mtick.FuncFormatter(usd))
    plt.tight_layout()
    plt.savefig(ASSETS / "02_category_revenue.png")
    plt.close()
    print("  ✓ 02_category_revenue.png")


# ── 3. Order Status Breakdown ──────────────────────────────────────────────────

def plot_order_status(df_all):
    status = df_all["order_status"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6",
              "#06b6d4", "#ec4899", "#84cc16"]
    wedges, texts, autotexts = ax.pie(
        status.values, labels=status.index, autopct="%1.1f%%",
        colors=colors[:len(status)], startangle=140
    )
    ax.set_title("Order Status Distribution")
    plt.tight_layout()
    plt.savefig(ASSETS / "03_order_status.png")
    plt.close()
    print("  ✓ 03_order_status.png")


# ── 4. Review Score Distribution ──────────────────────────────────────────────

def plot_review_scores(df):
    scores = df["review_score"].value_counts().sort_index()

    colors = ["#ef4444", "#f97316", "#f59e0b", "#84cc16", "#22c55e"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(scores.index, scores.values, color=colors, edgecolor="none", width=0.6)
    for i, (score, count) in enumerate(zip(scores.index, scores.values)):
        ax.text(score, count + 200, f"{count:,}", ha="center", fontsize=10)
    ax.set_title("Review Score Distribution")
    ax.set_xlabel("Review Score (1–5)")
    ax.set_ylabel("Number of Orders")
    ax.set_xticks([1, 2, 3, 4, 5])
    plt.tight_layout()
    plt.savefig(ASSETS / "04_review_scores.png")
    plt.close()
    print("  ✓ 04_review_scores.png")


# ── 5. Delivery Days Distribution ─────────────────────────────────────────────

def plot_delivery_days(df):
    delivery = df["delivery_days_actual"].dropna()
    delivery = delivery[(delivery >= 0) & (delivery <= 60)]

    fig, ax = plt.subplots()
    ax.hist(delivery, bins=40, color="#3b82f6", edgecolor="none", alpha=0.85)
    ax.axvline(delivery.mean(), color="#f59e0b", linewidth=2,
               linestyle="--", label=f"Mean: {delivery.mean():.1f} days")
    ax.axvline(delivery.median(), color="#10b981", linewidth=2,
               linestyle="--", label=f"Median: {delivery.median():.1f} days")
    ax.set_title("Delivery Time Distribution (Days)")
    ax.set_xlabel("Days to Deliver")
    ax.set_ylabel("Orders")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ASSETS / "05_delivery_days.png")
    plt.close()
    print("  ✓ 05_delivery_days.png")


# ── 6. Revenue by State (Top 10) ──────────────────────────────────────────────

def plot_state_revenue(df):
    state = (
        df.groupby("customer_state")["total_revenue"]
        .sum().sort_values(ascending=False).head(10)
    )

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(state.index, state.values, color="#3b82f6", edgecolor="none")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(usd))
    ax.set_title("Top 10 States by Revenue")
    ax.set_xlabel("State")
    plt.tight_layout()
    plt.savefig(ASSETS / "06_state_revenue.png")
    plt.close()
    print("  ✓ 06_state_revenue.png")


# ── 7. Payment Type Breakdown ──────────────────────────────────────────────────

def plot_payment_types(df):
    pay = df["payment_type"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444"]
    ax.bar(pay.index, pay.values, color=colors[:len(pay)], edgecolor="none")
    for i, (ptype, count) in enumerate(zip(pay.index, pay.values)):
        ax.text(i, count + 100, f"{count:,}", ha="center", fontsize=10)
    ax.set_title("Orders by Payment Type")
    ax.set_ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(ASSETS / "07_payment_types.png")
    plt.close()
    print("  ✓ 07_payment_types.png")


# ── 8. On-Time vs Late Delivery by State ──────────────────────────────────────

def plot_ontime_by_state(df):
    state_ot = (
        df.groupby("customer_state")["on_time_delivery"]
        .mean().mul(100).sort_values(ascending=True).tail(15)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#ef4444" if v < 85 else "#22c55e" for v in state_ot.values]
    ax.barh(state_ot.index, state_ot.values, color=colors, edgecolor="none")
    ax.axvline(90, color="#f59e0b", linestyle="--", linewidth=1.5, label="90% target")
    ax.set_title("On-Time Delivery Rate by State (%)")
    ax.set_xlabel("On-Time Delivery Rate (%)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ASSETS / "08_ontime_by_state.png")
    plt.close()
    print("  ✓ 08_ontime_by_state.png")


# ── 9. Avg Review Score by Category ──────────────────────────────────────────

def plot_review_by_category(df):
    cat_review = (
        df.groupby("category")["review_score"]
        .mean().sort_values(ascending=True).tail(15)
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#ef4444" if v < 3.5 else "#3b82f6" for v in cat_review.values]
    ax.barh(cat_review.index, cat_review.values, color=colors, edgecolor="none")
    ax.axvline(cat_review.mean(), color="#f59e0b", linestyle="--",
               linewidth=1.5, label=f"Avg: {cat_review.mean():.2f}")
    ax.set_title("Average Review Score by Category")
    ax.set_xlabel("Avg Review Score (1–5)")
    ax.legend()
    plt.tight_layout()
    plt.savefig(ASSETS / "09_review_by_category.png")
    plt.close()
    print("  ✓ 09_review_by_category.png")


# ── 10. Orders by Day of Week ─────────────────────────────────────────────────

def plot_orders_by_dow(df):
    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = df["purchase_dow"].value_counts().reindex(dow_order)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(dow.index, dow.values, color="#3b82f6", edgecolor="none")
    ax.set_title("Orders by Day of Week")
    ax.set_ylabel("Number of Orders")
    plt.tight_layout()
    plt.savefig(ASSETS / "10_orders_by_dow.png")
    plt.close()
    print("  ✓ 10_orders_by_dow.png")


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("Loading master dataset...")
    df_all = pd.read_csv(MASTER, parse_dates=["order_purchase_timestamp"])
    df = df_all[df_all["order_status"] == "delivered"].copy()
    print(f"  Delivered orders: {len(df):,}")

    print("\nGenerating charts...")
    plot_monthly_revenue(df)
    plot_category_revenue(df)
    plot_order_status(df_all)
    plot_review_scores(df)
    plot_delivery_days(df)
    plot_state_revenue(df)
    plot_payment_types(df)
    plot_ontime_by_state(df)
    plot_review_by_category(df)
    plot_orders_by_dow(df)

    print(f"\n✓ All charts saved to assets/")
    print("  → Use these in your case study and README")


if __name__ == "__main__":
    main()
