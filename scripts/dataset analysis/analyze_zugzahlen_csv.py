# Filename: analyze_zugzahlen_csv.py
# Location: scripts/dataset analysis/
"""
Analyze the structure and contents of zugzahlen.csv — train volumes per segment.

This script:
- Loads the CSV dataset using semicolon as delimiter
- Logs dataset shape, column names, sample rows, null value summary
- Reports data types and cardinalities for the first few columns

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/zugzahlen.csv"
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
# Main function
# ─────────────────────────────────────────────────────────────────────
def main():
    """
    Loads and summarizes the zugzahlen.csv dataset:
    - Logs basic structure and sample content
    - Prints dataset info and null value counts
    - Displays cardinality for first few columns
    """
    logging.info(f"📥 Loading file: {FILE_PATH}")

    try:
        df = pd.read_csv(FILE_PATH, sep=DELIMITER)
    except Exception as e:
        logging.error(f"❌ Failed to load CSV: {e}")
        sys.exit(1)

    logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

    # Print column names
    logging.info("🧾 Columns:")
    for col in df.columns:
        logging.info(f" - {col}")

    # Sample records
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # Dataset info
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # Null value summary
    logging.info("\n🧼 Null value summary:")
    print(df.isna().sum())

    # Cardinality preview
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        print(f" - {col}: {df[col].nunique()} unique")

# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
