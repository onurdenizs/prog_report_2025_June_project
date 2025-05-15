"""
map_gtfs_stops_to_sumo_nodes.py

Matches GTFS stops to the nearest SUMO nodes based on coordinates.
Outputs a mapping: stop_id → SUMO node_id, used for route generation.

Author: Onur Deniz
Date: 2025-05
"""

import os
import pandas as pd
import numpy as np
from scipy.spatial import KDTree
import logging

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────

GTFS_STOP_FILE = "data/Swiss/raw/gtfs/stops.txt"
SUMO_NODE_FILE = "data/Swiss/processed/rail_nodes_named.csv"
OUTPUT_MAPPING_FILE = "data/Swiss/interim/stop_mappings/stop_id_to_node_id.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ────────────────────────────────────────────────────────────────────────────────
# MAIN FUNCTION
# ────────────────────────────────────────────────────────────────────────────────

def map_gtfs_to_sumo(gtfs_file, sumo_node_file, output_file):
    logging.info("📥 Loading GTFS stops and SUMO nodes...")

    gtfs_df = pd.read_csv(gtfs_file)
    gtfs_df = gtfs_df.dropna(subset=["stop_lat", "stop_lon"])
    gtfs_coords = gtfs_df[["stop_id", "stop_lat", "stop_lon"]].copy()

    sumo_df = pd.read_csv(sumo_node_file)
    sumo_df = sumo_df.dropna(subset=["x", "y"])  # x = lon, y = lat
    sumo_coords = sumo_df[["node_id", "x", "y"]].copy()
    sumo_coords = sumo_coords.rename(columns={"node_id": "id"})  # unify naming downstream


    logging.info(f"✅ Loaded {len(gtfs_coords)} GTFS stops and {len(sumo_coords)} SUMO nodes.")

    # Build KD-tree for SUMO nodes (fast nearest neighbor lookup)
    tree = KDTree(sumo_coords[["y", "x"]].values)  # latitude, longitude

    # Find nearest SUMO node for each GTFS stop
    gtfs_latlon = gtfs_coords[["stop_lat", "stop_lon"]].values
    distances, indices = tree.query(gtfs_latlon)

    gtfs_coords["nearest_node_id"] = sumo_coords.iloc[indices]["id"].values
    gtfs_coords["distance_m"] = distances * 111000  # rough meters approximation

    logging.info("🔍 Nearest node mapping completed.")

    # Save results
    mapping_df = gtfs_coords[["stop_id", "nearest_node_id", "distance_m"]].rename(
        columns={"nearest_node_id": "node_id"}
    )

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    mapping_df.to_csv(output_file, index=False)
    logging.info(f"✅ Mapping file saved to {output_file}.")

# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    map_gtfs_to_sumo(GTFS_STOP_FILE, SUMO_NODE_FILE, OUTPUT_MAPPING_FILE)
