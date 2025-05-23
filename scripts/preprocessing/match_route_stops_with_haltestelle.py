import os
import logging
import pandas as pd

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
HALTESTELLE_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\haltestelle-haltekante.csv"
GTFS_STOP_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\gtfs\stop_times.txt"
OUTPUT_MATCHED_IDS = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\matched_stop_ids.txt"

# ----------------------------------------------------------------------------
# Logging setup
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------------------------------------------------------
# Utility
# ----------------------------------------------------------------------------
def clean_stop_id(raw_stop_id):
    """Extract numeric part from a stop_id, e.g. '8503054:0:1' -> '8503054'."""
    return str(raw_stop_id).split(':')[0]

# ----------------------------------------------------------------------------
# Main logic
# ----------------------------------------------------------------------------
def find_matched_stop_ids(haltestelle_path: str, gtfs_stop_times_path: str, output_path: str):
    """
    Finds stop_ids from GTFS stop_times.txt that are present in haltestelle-haltekante.csv

    Args:
        haltestelle_path (str): Path to haltestelle-haltekante.csv
        gtfs_stop_times_path (str): Path to GTFS stop_times.txt
        output_path (str): Where to save the matched stop_id list
    """
    logging.info("🔍 Starting matching of stop_ids between GTFS stop_times and Haltestelle...")

    try:
        df_halt = pd.read_csv(haltestelle_path, sep=';', dtype=str)
        logging.info(f"✅ Loaded haltestelle-haltekante.csv with shape: {df_halt.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load Haltestelle file: {e}")
        return

    try:
        df_gtfs = pd.read_csv(gtfs_stop_times_path, sep=',', dtype=str)
        logging.info(f"✅ Loaded stop_times.txt with shape: {df_gtfs.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load GTFS stop_times.txt: {e}")
        return

    if 'number' not in df_halt.columns or 'stop_id' not in df_gtfs.columns:
        logging.error("❌ Required columns 'number' in haltestelle or 'stop_id' in stop_times are missing.")
        return

    halt_ids = set(df_halt['number'].dropna().astype(str).str.strip())
    gtfs_raw_ids = df_gtfs['stop_id'].dropna().astype(str).apply(clean_stop_id)
    gtfs_ids = set(gtfs_raw_ids)

    matched_ids = sorted(halt_ids & gtfs_ids)

    # Save to file
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for sid in matched_ids:
                f.write(f"{sid}\n")
        logging.info(f"💾 Saved {len(matched_ids)} matched stop IDs to: {output_path}")
    except Exception as e:
        logging.error(f"❌ Failed to save matched stop IDs: {e}")
        return

    # Show sample
    print("\n🔍 Sample matched stop IDs:")
    for sid in matched_ids[:10]:
        print(f"  - {sid}")

    print("\n✅ Matching complete.\n")

# ----------------------------------------------------------------------------
# Execute
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    find_matched_stop_ids(HALTESTELLE_PATH, GTFS_STOP_PATH, OUTPUT_MATCHED_IDS)
