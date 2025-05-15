# Filename: analyze_rollmaterial_csv.py
# Location: scripts/dataset analysis/

import pandas as pd
import logging
import sys

# ──────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/rollmaterial.csv"
DELIMITER = ";"  # Semicolon-separated CSV

# ──────────────────────────────────────────────────────────────
# Logging setup
# ──────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ──────────────────────────────────────────────────────────────
# Main function
# ──────────────────────────────────────────────────────────────
def main():
    """
    Load and analyze the SBB rolling stock specification dataset.

    This script reads the file 'rollmaterial.csv', which contains
    descriptive details of SBB-owned passenger rolling stock,
    including configurations for specific vehicle structure types.

    The script prints:
    - Dataset dimensions and column names
    - A sample of the first few rows
    - Schema information with dtypes and non-null counts
    - Null value distribution
    - Cardinality preview for the first 5 columns
    """
    logging.info(f"📥 Loading file: {FILE_PATH}")

    try:
        df = pd.read_csv(FILE_PATH, sep=DELIMITER, low_memory=False)
    except Exception as e:
        logging.error(f"❌ Failed to load CSV: {e}")
        sys.exit(1)

    logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

    # ─────────────────────────────────────────────────────────
    # Column names
    # ─────────────────────────────────────────────────────────
    logging.info("🧾 Columns:")
    for col in df.columns:
        logging.info(f" - {col}")

    # ─────────────────────────────────────────────────────────
    # Sample rows
    # ─────────────────────────────────────────────────────────
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # ─────────────────────────────────────────────────────────
    # Dataset schema
    # ─────────────────────────────────────────────────────────
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # ─────────────────────────────────────────────────────────
    # Null value summary
    # ─────────────────────────────────────────────────────────
    logging.info("\n🧼 Null value summary:")
    print(df.isna().sum())

    # ─────────────────────────────────────────────────────────
    # Cardinality (number of unique values) preview
    # ─────────────────────────────────────────────────────────
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        unique_count = df[col].nunique()
        print(f" - {col}: {unique_count} unique")

# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()

