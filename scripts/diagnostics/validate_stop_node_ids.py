"""
validate_stop_node_ids.py

Checks how many node_ids in stop_id_to_node_id.csv exist in the compiled SUMO network.
Parses <junction> elements in .net.xml instead of <node>.

Author: Onur Deniz
Updated: 2025-05-09
"""

import xml.etree.ElementTree as ET
import pandas as pd
import time
import logging
import os

# === Configuration ===
NET_FILE = "SUMO/input/april_2025_swiss.net.xml"
MAPPING_FILE = "data/Swiss/interim/stop_mappings/stop_id_to_node_id.csv"
MISSING_CSV_OUT = "output/logs/missing_node_ids.csv"

# === Logging Setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info("📥 Reading SUMO .net.xml...")
    start = time.time()
    tree = ET.parse(NET_FILE)
    root = tree.getroot()

    sumo_nodes = {
        elem.attrib["id"]
        for elem in root.findall("junction")
        if "id" in elem.attrib
    }
    logging.info(f"✅ Loaded {len(sumo_nodes):,} nodes from SUMO in {time.time() - start:.1f} seconds.")

    logging.info("📥 Reading mapped stop-node file...")
    df = pd.read_csv(MAPPING_FILE)
    mapped_nodes = df["node_id"].dropna().unique()

    logging.info("🔍 Comparing node_id coverage...")
    missing = [nid for nid in mapped_nodes if nid not in sumo_nodes]

    # === Output Summary ===
    logging.info("\n🔍 SUMO Node Mapping Validation")
    logging.info(f"• Total mapped node IDs:        {len(mapped_nodes):,}")
    logging.info(f"• Present in SUMO network:      {len(mapped_nodes) - len(missing):,}")
    logging.info(f"• ❌ Missing from network:       {len(missing):,}")
    if missing:
        logging.warning(f"• ⚠️ Example missing node IDs:   {missing[:5]}")

        os.makedirs(os.path.dirname(MISSING_CSV_OUT), exist_ok=True)
        pd.Series(missing, name="missing_node_id").to_csv(MISSING_CSV_OUT, index=False)
        logging.info(f"💾 Missing node IDs saved to: {MISSING_CSV_OUT}")
    else:
        logging.info("✅ All mapped node IDs exist in the network.")

if __name__ == "__main__":
    main()
