# Filename: analyze_linienkilometrierung_csv.py
# Location: scripts/dataset analysis/

import pandas as pd
import logging
import sys

# ─────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/linienkilometrierung.csv"
DELIMITER = ";"  # CSV is semicolon-separated

# ─────────────────────────────────────────────────────────────────────
# Logging Setup
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
    """
    Load and analyze the 'linienkilometrierung.csv' dataset, which contains
    kilometrage mapping for the Swiss railway network.

    This script provides:
        - File loading with error handling
        - Column inspection
        - Sample data preview
        - Dataset schema information
        - Null value summary
        - Cardinality of first 5 columns
    """
    logging.info(f"📥 Loading file: {FILE_PATH}")
    
    try:
        df = pd.read_csv(FILE_PATH, sep=DELIMITER)
    except Exception as e:
        logging.error(f"❌ Failed to load the CSV file: {e}")
        sys.exit(1)

    logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

    # Column names
    logging.info("🧾 Columns:")
    for col in df.columns:
        logging.info(f" - {col}")

    # Display sample rows
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # Dataframe info
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # Null values per column
    logging.info("\n🧼 Null value summary:")
    print(df.isna().sum())

    # Cardinality preview (first 5 columns)
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        unique_vals = df[col].nunique()
        print(f" - {col}: {unique_vals} unique")

# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
