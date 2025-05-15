"""
generate_stop_node_mapping.py

Matches each GTFS stop to the nearest SUMO network node (rail node)
based on Euclidean distance using lat/lon vs. projected x/y.

Author: Onur Deniz
Date: 2025-05
"""

import os
import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
import logging

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────

GTFS_STOPS_FILE = "data/Swiss/raw/gtfs/stops.txt"
RAIL_NODES_FILE = "data/Swiss/processed/rail_nodes_named.csv"
OUTPUT_FILE = "data/Swiss/interim/stop_mappings/stop_id_to_node_id.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ────────────────────────────────────────────────────────────────────────────────
# MAIN LOGIC
# ────────────────────────────────────────────────────────────────────────────────

def generate_stop_node_mapping():
    logging.info("📥 Reading GTFS stops from %s...", GTFS_STOPS_FILE)
    stops_df = pd.read_csv(GTFS_STOPS_FILE)
    stops_df = stops_df.dropna(subset=["stop_lat", "stop_lon"])
    stops_df["stop_lat"] = stops_df["stop_lat"].astype(float)
    stops_df["stop_lon"] = stops_df["stop_lon"].astype(float)
    logging.info("✅ Loaded %d GTFS stops.", len(stops_df))

    logging.info("📥 Reading SUMO rail nodes from %s...", RAIL_NODES_FILE)
    nodes_df = pd.read_csv(RAIL_NODES_FILE)
    nodes_df = nodes_df.dropna(subset=["x", "y"])
    nodes_df["x"] = nodes_df["x"].astype(float)
    nodes_df["y"] = nodes_df["y"].astype(float)
    logging.info("✅ Loaded %d SUMO rail nodes.", len(nodes_df))

    # Convert stop lat/lon to NumPy array (note: assuming planar Euclidean distance is sufficient)
    gtfs_coords = stops_df[["stop_lon", "stop_lat"]].to_numpy()
    sumo_coords = nodes_df[["x", "y"]].to_numpy()

    # Build spatial index for SUMO nodes
    tree = cKDTree(sumo_coords)

    logging.info("🔍 Finding nearest node for each GTFS stop...")
    distances, indices = tree.query(gtfs_coords, k=1)

    stop_ids = stops_df["stop_id"].tolist()
    matched_node_ids = nodes_df.iloc[indices]["node_id"].tolist()

    mapping_df = pd.DataFrame({
        "stop_id": stop_ids,
        "node_id": matched_node_ids,
        "distance_m": distances
    })

    logging.info("✅ Completed mapping for %d stops.", len(mapping_df))

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    mapping_df.to_csv(OUTPUT_FILE, index=False)
    logging.info("💾 Mapping saved to: %s", OUTPUT_FILE)

# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    generate_stop_node_mapping()
