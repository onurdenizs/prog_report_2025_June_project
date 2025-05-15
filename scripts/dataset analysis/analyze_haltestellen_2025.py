"""
analyze_haltestellen_2025.py

Fixes CSV loading for Swiss haltestellen_2025.csv by using proper delimiter and quotechar.
Analyzes shape, columns, dtypes, nulls, and cardinality.

Author: Onur Deniz
"""

import pandas as pd
import logging
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/haltestellen_2025.csv"
DELIMITER = ","         # This file uses comma-separated values
QUOTECHAR = '"'         # Columns are quoted

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def analyze_csv(file_path: str) -> None:
    try:
        logging.info(f"📥 Loading file: {file_path}")
        df = pd.read_csv(file_path, sep=DELIMITER, quotechar=QUOTECHAR)

        logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

        logging.info("🧾 Columns:")
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

    except FileNotFoundError:
        logging.error(f"❌ File not found: {file_path}")
    except Exception as e:
        logging.error(f"❌ Error while processing file: {e}")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    analyze_csv(FILE_PATH)
