# Filename: analyze_actual_date_world_traffic_point_csv.py
# Location: scripts/dataset analysis/

import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/actual_date-world-traffic_point-2025-04-05.csv"
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
def main():
    """Main function to analyze the world traffic point data CSV file.

    This script reads and inspects the given CSV file:
    - Displays column names
    - Prints sample rows
    - Shows dataset shape and null value summary
    - Provides data types and cardinality of key fields

    Raises:
        FileNotFoundError: If the file path is incorrect.
        pd.errors.ParserError: If there are issues parsing the CSV.
    """
    logging.info(f"📥 Loading file: {FILE_PATH}")

    try:
        df = pd.read_csv(FILE_PATH, sep=DELIMITER)
    except FileNotFoundError:
        logging.error(f"❌ File not found: {FILE_PATH}")
        sys.exit(1)
    except pd.errors.ParserError as e:
        logging.error(f"❌ CSV parsing error: {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")
        sys.exit(1)

    logging.info(f"✅ Loaded dataset with shape: {df.shape}\n")

    # List columns
    logging.info("🧾 Columns:")
    for col in df.columns:
        logging.info(f" - {col}")

    # Show first 5 rows
    logging.info("\n🔍 Sample rows:")
    print(df.head(5).to_string(index=False))

    # General info
    logging.info("\n📊 Dataset Info:")
    print(df.info())

    # Null values per column
    logging.info("\n🧼 Null value summary:")
    print(df.isna().sum())

    # Cardinality for first 5 columns
    logging.info("\n📦 Cardinality preview (top 5 columns):")
    for col in df.columns[:5]:
        unique_count = df[col].nunique()
        print(f" - {col}: {unique_count} unique")


# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
