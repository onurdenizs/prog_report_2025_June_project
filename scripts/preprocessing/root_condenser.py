import os
import logging
import pandas as pd

# ----------------------------------------------------------------------------
# Logging Configuration
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ----------------------------------------------------------------------------
# Configuration Paths
# ----------------------------------------------------------------------------
STOP_TIMES_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\gtfs\stop_times.txt"
MATCHED_IDS_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\matched_stop_ids.txt"
OUTPUT_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\routes_condensed.csv"

# ----------------------------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------------------------
def clean_stop_id(raw_stop_id: str) -> str:
    """Extract numeric portion of stop_id (e.g. '8503054:0:1' -> '8503054')."""
    return str(raw_stop_id).split(":")[0]

# ----------------------------------------------------------------------------
# Main Processing Function
# ----------------------------------------------------------------------------
def create_condensed_routes():
    """
    Process stop_times.txt to generate routes_condensed.csv
    including only routes whose all stop_ids are matched with Haltestelle data.
    """
    logging.info("✨ Starting condensed route creation...")

    # Load matched stop IDs
    try:
        with open(MATCHED_IDS_PATH, 'r') as f:
            matched_ids = set(line.strip() for line in f if line.strip())
        logging.info(f"✅ Loaded {len(matched_ids)} matched stop IDs from {MATCHED_IDS_PATH}")
    except Exception as e:
        logging.error(f"Failed to load matched stop IDs: {e}")
        return

    # Load stop_times.txt
    try:
        df = pd.read_csv(STOP_TIMES_PATH, dtype=str)
        logging.info(f"✅ Loaded stop_times.txt with shape: {df.shape}")
    except Exception as e:
        logging.error(f"Failed to load stop_times.txt: {e}")
        return

    # Clean stop_ids and convert stop_sequence to int
    df['stop_id_clean'] = df['stop_id'].apply(clean_stop_id)
    df['stop_sequence'] = df['stop_sequence'].astype(int)

    # Group by trip_id and sort by stop_sequence
    grouped = df.sort_values(['trip_id', 'stop_sequence']).groupby('trip_id')

    valid_routes = []
    discarded_count = 0

    for trip_id, group in grouped:
        stops = list(group['stop_id_clean'])
        if all(sid in matched_ids for sid in stops):
            valid_routes.append({'trip_id': trip_id, 'stops': stops})
        else:
            discarded_count += 1

    # Save the result
    result_df = pd.DataFrame(valid_routes)
    try:
        result_df.to_csv(OUTPUT_PATH, sep=';', index=False)
        logging.info(f"📅 Saved {len(result_df)} valid routes to: {OUTPUT_PATH}")
        print(f"\n✅ Done! {len(result_df)} routes written to file. {discarded_count} routes were discarded.\n")
    except Exception as e:
        logging.error(f"Failed to save condensed route file: {e}")

# ----------------------------------------------------------------------------
# Execute
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    create_condensed_routes()
