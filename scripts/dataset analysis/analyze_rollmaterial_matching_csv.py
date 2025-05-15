"""
Filename: analyze_rollmaterial_matching_csv.py
Location: scripts/dataset analysis/

This script analyzes the structure and content of the file 'rollmaterial-matching.csv',
which is used to link vehicle type information between the rolling stock technical data
('rollmaterial.csv') and the train formation dataset ('jahresformation.csv').

The goal is to provide a clear overview of column structure, nulls, unique values, and data samples.
"""

import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/rollmaterial-matching.csv"
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
    """Main execution block for dataset structure and quality inspection."""
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
    
    # Show sample rows
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # Show detailed info
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # Null values summary
    logging.info("\n🧼 Null value summary:")
    print(df.isna().sum())

    # Cardinality of top 5 columns
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        print(f" - {col}: {df[col].nunique()} unique")

# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
