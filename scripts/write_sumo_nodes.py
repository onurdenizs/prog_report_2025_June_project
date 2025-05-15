"""
write_sumo_nodes.py

Phase 2 of the SUMO Swiss Network Pipeline (April 2025 edition).
Converts named rail nodes into SUMO .nod.xml format.

Input:
    - data/Swiss/processed/rail_nodes_named.csv

Output:
    - SUMO/input/april_2025_swiss.nod.xml

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import os
import logging
from xml.etree.ElementTree import Element, SubElement, ElementTree

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
INPUT_PATH = "data/Swiss/processed/rail_nodes_named.csv"
OUTPUT_PATH = "SUMO/input/april_2025_swiss.nod.xml"

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ─────────────────────────────────────────────────────────────────────────────
# Main function
# ─────────────────────────────────────────────────────────────────────────────
def main():
    logging.info("🚀 Phase 2: Generating SUMO .nod.xml from rail_nodes_named.csv...")

    if not os.path.exists(INPUT_PATH):
        logging.error(f"❌ Input file not found: {INPUT_PATH}")
        return

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    try:
        df = pd.read_csv(INPUT_PATH)
        required_cols = {"node_id", "x", "y"}
        if not required_cols.issubset(df.columns):
            raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")
    except Exception as e:
        logging.error(f"❌ Failed to read input file: {e}")
        return

    logging.info(f"✅ Loaded {len(df):,} nodes from: {INPUT_PATH}")

    # Build XML tree
    root = Element("nodes")

    for _, row in df.iterrows():
        SubElement(
            root,
            "node",
            id=row["node_id"],
            x=str(row["x"]),
            y=str(row["y"])
        )

    # Write to file
    tree = ElementTree(root)
    tree.write(OUTPUT_PATH, encoding="UTF-8", xml_declaration=True)
    logging.info(f"💾 Saved node XML to: {OUTPUT_PATH}")
    logging.info("✅ Phase 2 complete. Ready for Phase 3: write_sumo_edges.py")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
