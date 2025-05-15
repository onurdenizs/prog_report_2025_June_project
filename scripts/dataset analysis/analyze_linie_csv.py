"""
analyze_linie_csv.py

Analyzes the structure and content of 'linie.csv' from Swiss railway datasets.
This dataset is assumed to be semicolon-separated.

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/linie.csv"
ENCODING = "utf-8"
DELIMITER = ";"

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ─────────────────────────────────────────────────────────────────────────────
# Main analysis function
# ─────────────────────────────────────────────────────────────────────────────
def analyze_linie_csv(filepath: str, delimiter: str = ";"):
    logging.info(f"📥 Loading file: {filepath}")
    try:
        df = pd.read_csv(filepath, delimiter=delimiter, encoding=ENCODING)
    except Exception as e:
        logging.error(f"❌ Failed to load CSV: {e}")
        return

    logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

    # Display columns
    logging.info("🧾 Columns:")
    for col in df.columns:
        print(f" - {col}")
    
    # Display first few rows
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # Summary of data types and non-null counts
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # Check for nulls
    logging.info("\n🧼 Null value summary:")
    print(df.isnull().sum())

    # Unique values in key columns (if known)
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        unique_vals = df[col].nunique()
        print(f" - {col}: {unique_vals} unique")

# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    analyze_linie_csv(FILE_PATH, DELIMITER)
