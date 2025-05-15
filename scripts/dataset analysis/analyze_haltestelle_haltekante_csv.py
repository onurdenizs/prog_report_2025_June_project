"""
analyze_haltestelle_haltekante_csv.py

Exploratory analysis script for the Swiss public transport infrastructure dataset:
'haltestelle-haltekante.csv'. Inspects structure, content, nulls, and unique values.

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import logging
import sys
import os

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/haltestelle-haltekante.csv"
DELIMITER = ';'
ENCODING = 'utf-8'

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ─────────────────────────────────────────────────────────────────────────────
# Main analysis logic
# ─────────────────────────────────────────────────────────────────────────────
def analyze_csv(file_path: str):
    logging.info(f"📥 Loading file: {file_path}")
    try:
        df = pd.read_csv(file_path, delimiter=DELIMITER, encoding=ENCODING)
        logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")
        
        # Print column names
        logging.info("🧾 Columns:\n - " + "\n - ".join(df.columns))

        # Print first few rows
        logging.info("\n🔍 Sample rows:")
        print(df.head(5).to_string(index=False), end="\n\n")

        # General info
        logging.info("📊 Dataset Info:")
        print(df.info(), end="\n\n")

        # Null values summary
        logging.info("🧼 Null value summary:")
        print(df.isnull().sum(), end="\n\n")

        # Cardinality summary for first few columns
        logging.info("📦 Cardinality preview (top 5 columns):")
        for col in df.columns[:5]:
            print(f" - {col}: {df[col].nunique()} unique")

    except Exception as e:
        logging.error(f"❌ Failed to analyze CSV: {e}")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not os.path.exists(FILE_PATH):
        logging.error(f"❌ File not found: {FILE_PATH}")
        sys.exit(1)
    analyze_csv(FILE_PATH)
