"""
write_sumo_edges.py

Phase 3 of the SUMO Swiss Network Pipeline (April 2025 edition).
Converts enriched rail edges into SUMO-compatible .edg.xml format.

Each edge includes:
- Safe SUMO edge ID
- From/to node references
- Shape derived from LineString geometry (WKT)

Input:
    - data/Swiss/processed/rail_edges_named.csv

Output:
    - SUMO/input/april_2025_swiss.edg.xml

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import os
import logging
import re
from shapely import wkt
from shapely.geometry import LineString
from xml.etree.ElementTree import Element, SubElement, ElementTree

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
INPUT_PATH = "data/Swiss/processed/rail_edges_named.csv"
OUTPUT_PATH = "SUMO/input/april_2025_swiss.edg.xml"

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def linestring_to_shape(line: LineString) -> str:
    """
    Converts a Shapely LineString to a SUMO shape string (x1,y1 x2,y2 ...).
    """
    return " ".join([f"{x:.3f},{y:.3f}" for x, y, *_ in line.coords])

def sanitize_edge_id(edge_id: str) -> str:
    """
    Makes edge IDs safe for SUMO by replacing or removing invalid characters.
    """
    edge_id = str(edge_id)
    edge_id = edge_id.replace("&", "and")
    edge_id = re.sub(r"[ ,:()\.\\/\"']", "_", edge_id)
    edge_id = re.sub(r"__+", "_", edge_id)  # Collapse multiple underscores
    return edge_id.strip("_")

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main():
    logging.info("🚀 Phase 3: Generating SUMO .edg.xml from rail_edges_named.csv...")

    if not os.path.exists(INPUT_PATH):
        logging.error(f"❌ Input file not found: {INPUT_PATH}")
        return

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    try:
        df = pd.read_csv(INPUT_PATH)
        if not {"edge_id_human", "from_node", "to_node", "geometry"}.issubset(df.columns):
            raise ValueError("Missing one or more required columns.")
        df["geometry"] = df["geometry"].apply(wkt.loads)
    except Exception as e:
        logging.error(f"❌ Failed to load or parse input file: {e}")
        return

    logging.info(f"✅ Loaded {len(df):,} edges from: {INPUT_PATH}")

    root = Element("edges")
    failed_count = 0

    for i, row in df.iterrows():
        try:
            edge_id = sanitize_edge_id(row["edge_id_human"])
            attrib = {
                "id": edge_id,
                "from": row["from_node"],
                "to": row["to_node"]
            }

            if isinstance(row["geometry"], LineString):
                attrib["shape"] = linestring_to_shape(row["geometry"])
            else:
                raise ValueError("Invalid geometry")

            SubElement(root, "edge", attrib)

        except Exception as e:
            failed_count += 1
            logging.debug(f"⚠️ Skipping edge at row {i} due to error: {e}")
            continue

    # Write to .edg.xml
    tree = ElementTree(root)
    tree.write(OUTPUT_PATH, encoding="UTF-8", xml_declaration=True)

    logging.info(f"💾 Saved edge XML to: {OUTPUT_PATH}")
    logging.info(f"✅ Phase 3 complete. {len(df) - failed_count:,} edges written, {failed_count:,} skipped.")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
