"""
Script: generate_edge_anchor_nodes.py

Description:
This script finds the closest physical nodes for each rail segment in the linie_mit_polygon.csv file.
It uses the cleaned node file (simple_stops_edges_cleaned.csv) which maps each station to a line-specific node.

Output:
A file named edge_anchor_nodes.csv listing for each Linie segment:
- START_OP, END_OP
- Linie
- start_node_id, end_node_id (closest matching node from cleaned stop list)

Author: Onur Deniz
"""
import os
import logging
import pandas as pd
from shapely.geometry import LineString, Point

# =============================
# CONFIGURATION
# =============================
INPUT_LINIE_POLYGON = r"D:/PhD/prog_report_2025_June_project/data/Swiss/raw/linie_mit_polygon.csv"
INPUT_NODES = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/simple_stops_edges_cleaned.csv"
OUTPUT_CSV = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/edge_anchor_nodes.csv"

# =============================
# LOGGING SETUP
# =============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def extract_midpoint_coords(geo_shape_str):
    """Extract midpoint coordinates from GeoJSON-style LineString string."""
    try:
        geojson = eval(geo_shape_str)
        coords = geojson["coordinates"]
        line = LineString(coords)
        mid_point = line.interpolate(0.5, normalized=True)
        return mid_point.x, mid_point.y
    except Exception as e:
        logger.warning(f"Failed to parse geometry: {e}")
        return None, None

def main():
    logger.info("\U0001F4C5 Loading input files...")

    try:
        df_segments = pd.read_csv(INPUT_LINIE_POLYGON, sep=';', dtype=str)
        df_nodes = pd.read_csv(INPUT_NODES, dtype=str)
    except Exception as e:
        logger.error(f"Failed to load input files: {e}")
        return

    df_segments = df_segments[['START_OP', 'END_OP', 'Linie', 'Geo shape']].dropna()
    df_nodes['Linie'] = df_nodes['Linie'].astype(str)

    logger.info("\U0001F517 Finding closest anchor nodes for each segment...")
    records = []

    for idx, row in df_segments.iterrows():
        start_op, end_op, linie, shape_str = row['START_OP'], row['END_OP'], str(row['Linie']), row['Geo shape']
        mid_x, mid_y = extract_midpoint_coords(shape_str)
        if mid_x is None:
            continue

        # Candidates filtered by Linie number
        candidates = df_nodes[df_nodes['Linie'] == linie]
        if candidates.empty:
            continue

        start_candidates = candidates[candidates['stop_abbr'] == start_op]
        end_candidates = candidates[candidates['stop_abbr'] == end_op]

        def find_nearest(candidates_df):
            candidates_df = candidates_df.copy()
            candidates_df[['x', 'y']] = candidates_df[['x', 'y']].astype(float)
            candidates_df['dist'] = ((candidates_df['x'] - mid_x)**2 + (candidates_df['y'] - mid_y)**2)**0.5
            return candidates_df.sort_values('dist').iloc[0]['physical_node_id'] if not candidates_df.empty else None

        node_start = find_nearest(start_candidates)
        node_end = find_nearest(end_candidates)

        if node_start and node_end:
            records.append({
                'Linie': linie,
                'START_OP': start_op,
                'END_OP': end_op,
                'START_NODE': node_start,
                'END_NODE': node_end
            })

    if records:
        df_result = pd.DataFrame(records)
        df_result.to_csv(OUTPUT_CSV, index=False)
        logger.info(f"✅ Anchor nodes saved to: {OUTPUT_CSV}")
        print(f"\n🎯 Done!\n✅ Segments mapped: {len(df_result)}\n📁 Output: {OUTPUT_CSV}")
    else:
        logger.warning("⚠️ No valid mappings found. Output will be empty.")
        pd.DataFrame(columns=['Linie','START_OP','END_OP','START_NODE','END_NODE']).to_csv(OUTPUT_CSV, index=False)

if __name__ == "__main__":
    main()
