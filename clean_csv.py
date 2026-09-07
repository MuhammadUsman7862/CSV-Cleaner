#!/usr/bin/env python3
"""
clean_csv.py

Reads a CSV file with pandas, cleans missing values, and writes a cleaned
CSV to disk. Designed to be simple, readable, and easy to extend.

Usage:
    python clean_csv.py input.csv
    python clean_csv.py input.csv --output cleaned.csv
    python clean_csv.py input.csv --strategy mean
    python clean_csv.py input.csv --drop-threshold 0.5
"""

import argparse
import sys
from pathlib import Path

import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load a CSV file into a DataFrame, exiting with a clear error if it fails."""
    file_path = Path(path)
    if not file_path.exists():
        print(f"Error: file not found -> {path}", file=sys.stderr)
        sys.exit(1)

    try:
        df = pd.read_csv(file_path)
    except Exception as exc:
        print(f"Error reading CSV: {exc}", file=sys.stderr)
        sys.exit(1)

    return df


def summarize_missing(df: pd.DataFrame) -> None:
    """Print a quick summary of missing values per column."""
    missing = df.isna().sum()
    missing = missing[missing > 0]

    if missing.empty:
        print("No missing values found.")
        return

    print("Missing values before cleaning:")
    for col, count in missing.items():
        pct = (count / len(df)) * 100
        print(f"  - {col}: {count} missing ({pct:.1f}%)")


def drop_sparse_columns(df: pd.DataFrame, threshold: float) -> pd.DataFrame:
    """Drop columns where the fraction of missing values exceeds `threshold`."""
    if threshold >= 1.0:
        return df

    missing_frac = df.isna().mean()
    cols_to_drop = missing_frac[missing_frac > threshold].index.tolist()

    if cols_to_drop:
        print(f"Dropping columns with >{threshold * 100:.0f}% missing: {cols_to_drop}")
        df = df.drop(columns=cols_to_drop)

    return df


def fill_missing(df: pd.DataFrame, strategy: str) -> pd.DataFrame:
    """
    Fill missing values based on the chosen strategy.

    Strategies:
        - "drop": drop any row containing a missing value
        - "mean": fill numeric columns with column mean, text columns with "Unknown"
        - "median": fill numeric columns with column median, text columns with "Unknown"
        - "zero": fill numeric columns with 0, text columns with "Unknown"
    """
    if strategy == "drop":
        before = len(df)
        df = df.dropna()
        print(f"Dropped {before - len(df)} rows containing missing values.")
        return df

    numeric_cols = df.select_dtypes(include="number").columns
    text_cols = df.select_dtypes(exclude="number").columns

    if strategy == "mean":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == "median":
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    elif strategy == "zero":
        df[numeric_cols] = df[numeric_cols].fillna(0)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    df[text_cols] = df[text_cols].fillna("Unknown")
    return df


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Drop exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        print(f"Removed {removed} duplicate row(s).")
    return df


def clean_dataframe(df: pd.DataFrame, strategy: str, drop_threshold: float) -> pd.DataFrame:
    """Run the full cleaning pipeline on a DataFrame."""
    summarize_missing(df)
    df = drop_sparse_columns(df, drop_threshold)
    df = fill_missing(df, strategy)
    df = remove_duplicates(df)
    return df


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read a CSV, clean missing values, and save the result."
    )
    parser.add_argument("input", help="Path to the input CSV file")
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write the cleaned CSV (default: <input>_cleaned.csv)",
    )
    parser.add_argument(
        "--strategy",
        choices=["drop", "mean", "median", "zero"],
        default="mean",
        help="How to handle missing values (default: mean)",
    )
    parser.add_argument(
        "--drop-threshold",
        type=float,
        default=0.5,
        help="Drop columns with more than this fraction missing (default: 0.5)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    output_path = args.output
    if output_path is None:
        input_path = Path(args.input)
        output_path = str(input_path.with_name(f"{input_path.stem}_cleaned.csv"))

    print(f"Loading: {args.input}")
    df = load_csv(args.input)
    print(f"Loaded {len(df)} rows, {len(df.columns)} columns.\n")

    df = clean_dataframe(df, strategy=args.strategy, drop_threshold=args.drop_threshold)

    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    print(f"Final shape: {df.shape[0]} rows, {df.shape[1]} columns.")


if __name__ == "__main__":
    main()
