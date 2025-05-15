"""
extract_stop_edge_matches.py

This script processes the 'linie_mit_polygon.csv' dataset and extracts mappings between logical Swiss railway stops
and their corresponding physical edge coordinates. It supports Option B — where a single station (e.g., Grüsch) may 
have multiple coordinates due to multiple tracks. The script assigns physical node IDs (e.g., GRUS_A, GRUS_B) and 
outputs a CSV mapping logical stop names to all physical nodes. It also logs and prints detailed statistics about
stops with multiple coordinates.

Author: [Your Name]
Date: [Date]
"""

import os
import json
import logging
from collections import defaultdict
from typing import Dict, List, Tuple

import pandas as pd

# ----------------------------
# Configuration
# ----------------------------

INPUT_FILE = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\linie_mit_polygon.csv"
OUTPUT_DIR = r"D:\PhD\prog_report_2025_June_project\data\Swiss\processed\simpler_network"
OUTPUT_FILE = "simple_stops_edges.csv"
LOG_FILE = os.path.join(OUTPUT_DIR, "extract_stop_edge_matches_optionB.log")

# ----------------------------
# Logging Setup
# ----------------------------

os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------
# Helper Functions
# ----------------------------

def sanitize_name(name: str) -> str:
    """Sanitize a name to be SUMO-compatible by replacing problematic characters."""
    return name.strip().replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_")

def generate_physical_id(base_abbr: str, index: int) -> str:
    """Generate a physical node ID like GRUS_A, GRUS_B, etc."""
    return f"{base_abbr}_{chr(65 + index)}"

def extract_coordinates(df: pd.DataFrame) -> Dict[Tuple[str, str], set]:
    """
    Extracts and groups unique coordinates for each stop based on line geometry.
    
    Returns:
        Dictionary mapping (logical stop name, stop abbreviation) to a set of (lat, lon) coordinates.
    """
    coord_map = defaultdict(set)

    for idx, row in df.iterrows():
        try:
            shape = json.loads(row['Geo shape'])
            coords = shape.get("coordinates", [])
            if len(coords) < 2:
                logging.warning(f"Row {idx} skipped: insufficient coordinates.")
                continue

            # Read and sanitize stop identifiers
            start_name = sanitize_name(row['START_OP.1'])
            start_abbr = sanitize_name(row['START_OP'])
            end_name = sanitize_name(row['END_OP.1'])
            end_abbr = sanitize_name(row['END_OP'])

            # Get first and last coordinates, convert to (lat, lon)
            start_coord = tuple(reversed(coords[0]))
            end_coord = tuple(reversed(coords[-1]))

            coord_map[(start_name, start_abbr)].add(start_coord)
            coord_map[(end_name, end_abbr)].add(end_coord)

        except Exception as e:
            logging.error(f"Row {idx} skipped due to parsing error: {e}")

    return coord_map

def save_stop_edge_mapping(coord_map: Dict[Tuple[str, str], set], output_path: str):
    """
    Saves the stop-edge mapping into a CSV and prints diagnostics to the terminal.
    
    Args:
        coord_map: Dictionary of stop → set of coordinates
        output_path: Full path to the output CSV
    """
    print("\n📦 Generating output CSV and mapping physical nodes...")

    records = []
    multi_coord_stops = {}

    for (stop_name, stop_abbr), coords in coord_map.items():
        sorted_coords = sorted(coords)  # Ensure reproducibility
        if len(sorted_coords) > 1:
            multi_coord_stops[(stop_name, stop_abbr)] = sorted_coords

        for i, (lat, lon) in enumerate(sorted_coords):
            physical_node = generate_physical_id(stop_abbr, i)
            records.append({
                "logical_stop_name": stop_name,
                "stop_abbr": stop_abbr,
                "physical_node_id": physical_node,
                "lat": lat,
                "lon": lon
            })

    # Write to CSV
    df_out = pd.DataFrame(records)
    df_out.to_csv(output_path, index=False)
    logging.info(f"Output CSV saved to: {output_path}")

    # Terminal summary
    print("✅ Stop-edge extraction complete.")
    print(f"📍 Total logical stops detected: {len(coord_map)}")
    print(f"🔁 Total physical node entries written: {len(records)}")
    print(f"⚠️  Stops with multiple coordinate representations: {len(multi_coord_stops)}")

    if multi_coord_stops:
        print("\n🧭 Stops with multiple tracks or spatial representations:")
        for (name, abbr), coord_list in multi_coord_stops.items():
            print(f"  {name} ({abbr}):")
            for lat, lon in coord_list:
                print(f"    → {lat}, {lon}")

# ----------------------------
# Main Execution
# ----------------------------

def main():
    """Main execution function."""
    print("🚆 Starting station-to-edge extraction (Option B)...")
    print(f"📂 Reading from: {INPUT_FILE}")

    try:
        df = pd.read_csv(INPUT_FILE, sep=";", encoding="utf-8")
        print(f"📄 Loaded {len(df)} rows from dataset.")

        coord_map = extract_coordinates(df)
        print(f"🧹 Processed station mappings. Unique logical stops: {len(coord_map)}")

        output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
        save_stop_edge_mapping(coord_map, output_path)

        print("\n🎉 All done. Review CSV and logs for full details.")
        print(f"📁 CSV: {output_path}")
        print(f"📝 Log: {LOG_FILE}")

    except Exception as e:
        print(f"❌ Script failed with error: {e}")
        logging.error(f"Script terminated with exception: {e}")

if __name__ == "__main__":
    main()
