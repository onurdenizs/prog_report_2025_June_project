# Filename: extract_simplified_edges.py
# Location: D:/PhD/prog_report_2025_June_project/scripts/simple_network_creators/

import os
import sys
import logging
import pandas as pd

# ─────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────
INPUT_CSV = "D:/PhD/prog_report_2025_June_project/data/Swiss/raw/linie_mit_polygon.csv"
OUTPUT_CSV = "D:/PhD/prog_report_2025_June_project/data/Swiss/interim/simplified_edges.csv"
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
# Main execution
# ─────────────────────────────────────────────────────────────────────
def main():
    logging.info(f"📥 Loading raw simplified line geometry from: {INPUT_CSV}")

    try:
        df = pd.read_csv(INPUT_CSV, sep=DELIMITER)
    except Exception as e:
        logging.error(f"❌ Failed to load input file: {e}")
        sys.exit(1)

    # Validate column presence
    required_cols = {'START_OP', 'END_OP', 'START_OP.1', 'END_OP.1', 'Linie', 'Line', 'Geo shape'}
    if not required_cols.issubset(df.columns):
        logging.error(f"❌ Missing one or more required columns: {required_cols}")
        sys.exit(1)

    # Generate clean edge IDs
    df['edge_id'] = df.apply(
        lambda row: f"{str(row['Line']).strip().replace(' ', '_')}_{row['START_OP']}_{row['END_OP']}", axis=1
    )

    # Rename columns for consistency
    output_df = df[[
        'edge_id',
        'START_OP',
        'START_OP.1',
        'END_OP',
        'END_OP.1',
        'Linie',
        'Line',
        'Geo shape'
    ]].copy()

    output_df.columns = [
        'edge_id',
        'from_stop_id',
        'from_stop_name',
        'to_stop_id',
        'to_stop_name',
        'line_number',
        'line_name',
        'geometry_wkt'
    ]

    try:
        output_df.to_csv(OUTPUT_CSV, sep=";", index=False)
        logging.info(f"✅ Simplified edges saved to: {OUTPUT_CSV}")
        print(output_df.head(3).to_string(index=False))
    except Exception as e:
        logging.error(f"❌ Failed to write output file: {e}")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
