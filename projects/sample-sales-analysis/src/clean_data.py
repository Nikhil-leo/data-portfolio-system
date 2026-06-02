"""
clean_data.py — Data cleaning script for Sales Performance Analysis
Run: python src/clean_data.py
"""
import pandas as pd
from pathlib import Path

RAW = Path("data/raw/raw_data.csv")
OUT = Path("data/cleaned/cleaned_data.csv")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    print(f"  Raw shape: {df.shape}")

    # Remove exact duplicates
    df = df.drop_duplicates()

    # Standardize column names: lowercase with underscores
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    # Parse date columns — adapt column names to match your dataset
    for date_col in ["order_date", "ship_date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Fill missing numeric values with column median
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        null_count = df[col].isna().sum()
        if null_count > 0:
            df[col] = df[col].fillna(df[col].median())
            print(f"  Filled {null_count} nulls in '{col}' with median")

    # Fill missing string values with "Unknown"
    string_cols = df.select_dtypes(include="object").columns
    for col in string_cols:
        null_count = df[col].isna().sum()
        if null_count > 0:
            df[col] = df[col].fillna("Unknown")
            print(f"  Filled {null_count} nulls in '{col}' with 'Unknown'")

    print(f"  Cleaned shape: {df.shape}")
    return df


def main():
    if not RAW.exists():
        print(f"ERROR: Raw file not found at {RAW}")
        print("  Download the Superstore dataset from Kaggle and place it at data/raw/raw_data.csv")
        return

    print("Loading data...")
    df = pd.read_csv(RAW)

    print("Cleaning...")
    df = clean(df)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"\n✓ Saved {len(df):,} rows → {OUT}")


if __name__ == "__main__":
    main()
