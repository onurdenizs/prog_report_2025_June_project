"""
Diagnostic script to compare stop IDs from haltestelle-haltekante.csv and corrected_stops.txt.
Logs unique ID counts, matches, and sample unmatched IDs.
"""

import os
import logging
import pandas as pd

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
HALTESTELLE_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\haltestelle-haltekante.csv"
CORRECTED_STOPS_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\gtfs\corrected_stops.txt"

# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------------------------------
# Main diagnostic function
# -----------------------------------------------------------------------------
def compare_stop_ids(file1: str, file2: str):
    """
    Compares stop IDs from haltestelle-haltekante.csv and corrected_stops.txt.

    Args:
        file1 (str): Path to haltestelle-haltekante.csv.
        file2 (str): Path to corrected_stops.txt.
    """
    logging.info("🚦 Starting comparison between Haltestelle and corrected GTFS stop IDs...")

    try:
        df_halt = pd.read_csv(file1, sep=';', dtype=str)
        logging.info(f"✅ Loaded haltestelle-haltekante.csv with shape: {df_halt.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load haltestelle file: {e}")
        return

    try:
        df_gtfs = pd.read_csv(file2, dtype=str)
        logging.info(f"✅ Loaded corrected_stops.txt with shape: {df_gtfs.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load corrected stops file: {e}")
        return

    if 'number' not in df_halt.columns or 'stop_id' not in df_gtfs.columns:
        logging.error("❌ Required columns 'number' or 'stop_id' are missing.")
        return

    halt_ids = set(df_halt['number'].dropna().astype(str).str.strip())
    gtfs_ids = set(df_gtfs['stop_id'].dropna().astype(str).str.strip())

    matched = halt_ids & gtfs_ids
    only_in_halt = halt_ids - gtfs_ids
    only_in_gtfs = gtfs_ids - halt_ids

    # Logging results
    logging.info("\n📊 Comparison Results:")
    logging.info(f"  • Unique stop IDs in haltestelle-haltekante.csv : {len(halt_ids)}")
    logging.info(f"  • Unique stop IDs in corrected_stops.txt        : {len(gtfs_ids)}")
    logging.info(f"  • Matching stop IDs                             : {len(matched)}")
    logging.info(f"  • IDs only in haltestelle-haltekante.csv        : {len(only_in_halt)}")
    logging.info(f"  • IDs only in corrected_stops.txt               : {len(only_in_gtfs)}")

    # Show samples
    print("\n🔍 Sample unmatched stop IDs from haltestelle-haltekante.csv:")
    for sid in list(only_in_halt)[:10]:
        print(f"  - {sid}")

    print("\n🔍 Sample unmatched stop IDs from corrected_stops.txt:")
    for sid in list(only_in_gtfs)[:10]:
        print(f"  - {sid}")

    print("\n✅ Diagnostic complete.\n")

# -----------------------------------------------------------------------------
# Execute
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    compare_stop_ids(HALTESTELLE_PATH, CORRECTED_STOPS_PATH)
