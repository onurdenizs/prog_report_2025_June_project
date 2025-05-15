"""
analyze_linie_mit_polygon.py

Analyzes the structure and content of 'linie_mit_polygon.csv' to support simplified SUMO network generation.

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import logging
import sys

# ───────────────────────────────────────────────────────────────
# Configuration
# ───────────────────────────────────────────────────────────────
FILE_PATH = "data/Swiss/raw/linie_mit_polygon.csv"
DELIMITER = ';'

# ───────────────────────────────────────────────────────────────
# Logging setup
# ───────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ───────────────────────────────────────────────────────────────
# Main analysis function
# ───────────────────────────────────────────────────────────────
def analyze_linie_dataset(path):
    try:
        logging.info(f"📥 Loading dataset from: {path}")
        df = pd.read_csv(path, sep=DELIMITER, encoding="utf-8")
        logging.info(f"✅ Loaded file with shape: {df.shape}")

        # Print column names
        print("\n🧾 Columns:")
        for col in df.columns:
            print(f" - {col}")

        # Show sample data
        print("\n🔍 Sample rows:")
        print(df.head(5).to_string(index=False))

        # Analyze specific fields
        print("\n📊 Summary:")
        if 'linie' in df.columns:
            print(f" • Unique 'linie' IDs: {df['linie'].nunique()}")
        if 'spurweite' in df.columns:
            print(f" • Track gauges: {df['spurweite'].dropna().unique()}")
        if 'geo_shape' in df.columns:
            nulls = df['geo_shape'].isna().sum()
            print(f" • Missing geo_shape entries: {nulls}")

        if {'betriebsstelle_von', 'betriebsstelle_bis'}.issubset(df.columns):
            print(f" • Unique start points: {df['betriebsstelle_von'].nunique()}")
            print(f" • Unique end points: {df['betriebsstelle_bis'].nunique()}")

    except FileNotFoundError:
        logging.error(f"❌ File not found at path: {path}")
    except Exception as e:
        logging.error(f"❌ Unexpected error: {e}")

# ───────────────────────────────────────────────────────────────
# Entry point
# ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    analyze_linie_dataset(FILE_PATH)
