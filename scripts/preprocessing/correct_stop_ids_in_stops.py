"""
Script to normalize stop_id values in GTFS stops.txt by stripping suffixes and prefixes.
Creates a corrected version of the file named 'corrected_stops.txt'.

Examples of corrections:
- '8506894:0:10000' -> '8506894'
- 'Parent1107235'   -> '1107235'
"""

import os
import logging
import pandas as pd

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
STOPS_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\gtfs\stops.txt"
OUTPUT_PATH = os.path.join(os.path.dirname(STOPS_PATH), "corrected_stops.txt")

# -----------------------------------------------------------------------------
# Logging setup
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------------------------------------------------------
# Helper function
# -----------------------------------------------------------------------------
def normalize_stop_id(raw_id):
    """Normalizes stop_id by removing GTFS suffixes or 'Parent' prefix."""
    if isinstance(raw_id, str):
        if raw_id.startswith("Parent"):
            return raw_id.replace("Parent", "")
        return raw_id.split(":")[0]
    return str(raw_id)

# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
def correct_stop_ids(input_path: str, output_path: str):
    """
    Loads a GTFS stops.txt file, normalizes stop IDs, and saves a corrected version.

    Args:
        input_path (str): Path to the original stops.txt file.
        output_path (str): Path where the corrected file will be saved.
    """
    logging.info("🚀 Starting stop ID correction for stops.txt...")
    
    try:
        df = pd.read_csv(input_path, dtype=str)
        logging.info(f"✅ Loaded stops.txt with shape: {df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load stops.txt: {e}")
        return

    if 'stop_id' not in df.columns:
        logging.error("❌ 'stop_id' column is missing in the file.")
        return

    original_ids = df['stop_id'].unique()
    df['stop_id'] = df['stop_id'].apply(normalize_stop_id)
    corrected_ids = df['stop_id'].unique()

    logging.info("🔍 Correction Summary:")
    logging.info(f"  • Original unique stop IDs: {len(original_ids)}")
    logging.info(f"  • Corrected unique stop IDs: {len(corrected_ids)}")
    logging.info("  • Sample corrected pairs (before → after):")
    for orig, corr in zip(original_ids, df['stop_id'].unique()):
        if orig != corr:
            logging.info(f"    - {orig} → {corr}")
        if len(set(df['stop_id'].unique())) > 10:
            break

    try:
        df.to_csv(output_path, index=False)
        logging.info(f"🎉 Saved corrected stop IDs to: {output_path}")
    except Exception as e:
        logging.error(f"❌ Failed to write corrected file: {e}")
        return

    print(f"\n✅ Correction complete. File saved as:\n  {output_path}")

# -----------------------------------------------------------------------------
# Execute
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    correct_stop_ids(STOPS_PATH, OUTPUT_PATH)
