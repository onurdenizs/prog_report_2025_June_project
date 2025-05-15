# analyze_dienststellen_csv.py

"""
Analyzes the dataset 'dienststellen-gemass-opentransportdataswiss.csv',
which contains official Swiss stop/station information from opentransportdata.ch.

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/dienststellen-gemass-opentransportdataswiss.csv"
DELIMITER = ";"

# ─────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ─────────────────────────────────────────────────────────────────────
# Main analysis logic
# ─────────────────────────────────────────────────────────────────────
def analyze_dataset():
    try:
        logging.info(f"📥 Loading file: {FILE_PATH}")
        df = pd.read_csv(FILE_PATH, delimiter=DELIMITER)
        logging.info(f"✅ Loaded dataset with shape: {df.shape}")

        logging.info("\n🧾 Columns:")
        for col in df.columns:
            print(f" - {col}")

        logging.info("\n🔍 Sample rows:")
        print(df.head(5).to_string(index=False))

        logging.info("\n📊 Dataset Info:")
        print(df.info())

        logging.info("\n🧼 Null value summary:")
        print(df.isnull().sum())

        logging.info("\n📦 Cardinality preview (top 5 columns):")
        for col in df.columns[:5]:
            print(f" - {col}: {df[col].nunique()} unique")

    except Exception as e:
        logging.error(f"❌ Failed to analyze dataset: {e}")

# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    analyze_dataset()
