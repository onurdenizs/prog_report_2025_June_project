"""
extract_nodes_and_edges.py

Phase 1 of the SUMO Swiss Network Pipeline (April 2025 edition).
Extracts and projects raw railway nodes and edges from SwissTNE GeoPackage (LV95),
and saves them to CSV files for SUMO conversion.

Author: Onur Deniz
Date: 2025-05
"""

import geopandas as gpd
import pandas as pd
import logging
import os
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
INPUT_GPKG = "data/Swiss/raw/swissTNE_Base_20240507.gpkg"
OUTPUT_DIR = "data/Swiss/processed/"
NODE_LAYER = "bn_node"
EDGE_LAYER = "bn_edge"
CRS_TARGET = 2056  # EPSG:2056 (LV95 / CH1903+)

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ─────────────────────────────────────────────────────────────────────────────
# Helper: Load + Project GeoPackage Layer
# ─────────────────────────────────────────────────────────────────────────────
def load_and_project_layer(gpkg_path, layer_name, target_crs):
    """Loads a layer from GeoPackage, reprojects to target CRS."""
    try:
        logging.info(f"📂 Reading layer '{layer_name}' from {gpkg_path}...")
        gdf = gpd.read_file(gpkg_path, layer=layer_name)
        logging.info(f"✅ Loaded {len(gdf)} rows from '{layer_name}'")
        return gdf.to_crs(epsg=target_crs)
    except Exception as e:
        logging.error(f"❌ Failed to load layer '{layer_name}': {e}")
        sys.exit(1)

# ─────────────────────────────────────────────────────────────────────────────
# Main logic
# ─────────────────────────────────────────────────────────────────────────────
def main():
    logging.info("🚆 Phase 1: Extracting nodes and edges from SwissTNE...")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Load and export nodes ────────────────────────────────────────────────
    gdf_nodes = load_and_project_layer(INPUT_GPKG, NODE_LAYER, CRS_TARGET)
    gdf_nodes["node_id"] = "n_" + gdf_nodes["object_id"].astype(str)
    gdf_nodes["x"] = gdf_nodes.geometry.x
    gdf_nodes["y"] = gdf_nodes.geometry.y

    node_cols = ["node_id", "object_id", "x", "y", "geometry"]
    node_outfile = os.path.join(OUTPUT_DIR, "rail_nodes.csv")
    gdf_nodes[node_cols].to_csv(node_outfile, index=False)
    logging.info(f"💾 Saved {len(gdf_nodes):,} nodes → {node_outfile}")

    # ── Load and export edges ────────────────────────────────────────────────
    gdf_edges = load_and_project_layer(INPUT_GPKG, EDGE_LAYER, CRS_TARGET)
    gdf_edges["edge_id"] = "e_" + gdf_edges["object_id"].astype(str)
    gdf_edges["from_node"] = "n_" + gdf_edges["from_node_object_id"].astype(str)
    gdf_edges["to_node"] = "n_" + gdf_edges["to_node_object_id"].astype(str)
    gdf_edges["length"] = gdf_edges["m_length"]

    edge_cols = ["edge_id", "object_id", "from_node", "to_node", "length", "geometry"]
    edge_outfile = os.path.join(OUTPUT_DIR, "rail_edges.csv")
    gdf_edges[edge_cols].to_csv(edge_outfile, index=False)
    logging.info(f"💾 Saved {len(gdf_edges):,} edges → {edge_outfile}")

    logging.info("✅ Phase 1 complete. Ready for Phase 2: write_sumo_nodes.py")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
