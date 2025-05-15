"""
Analyze Jahresformation Dataset (jahresformation.csv)

This script analyzes the annual train formation dataset provided by SBB.
It provides a detailed summary of column names, sample records, data types,
null value counts, and unique cardinality of key fields.

- Source: data/Swiss/raw/jahresformation.csv
- Delimiter: ;
"""

import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/jahresformation.csv"
DELIMITER = ";"

# ─────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ─────────────────────────────────────────────────────────────────────
# Main Function
# ─────────────────────────────────────────────────────────────────────
def main():
    logging.info(f"📥 Loading file: {FILE_PATH}")

    # Try reading the CSV file
    try:
        df = pd.read_csv(FILE_PATH, sep=DELIMITER, low_memory=False)
    except FileNotFoundError:
        logging.error("❌ File not found. Please check the path and filename.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"❌ Failed to load CSV: {e}")
        sys.exit(1)

    logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

    # Display column names
    logging.info("🧾 Columns:")
    for col in df.columns:
        logging.info(f" - {col}")
    
    # Display first 5 rows as sample
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # Display dataset info
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # Show null value summary
    logging.info("\n🧼 Null value summary:")
    print(df.isna().sum())

    # Show unique values (cardinality) for the first 5 columns
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        print(f" - {col}: {df[col].nunique()} unique")

# ─────────────────────────────────────────────────────────────────────
# Entry Point
# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
