# Filename: write_simplified_edges_xml.py
# Location: D:/PhD/prog_report_2025_June_project/scripts/simple_network_creators/

import pandas as pd
import logging
import xml.etree.ElementTree as ET
import os
import sys

# ──────────────────────────────────────────────────────────────────────────────
# Configuration
# ──────────────────────────────────────────────────────────────────────────────
INPUT_CSV = "D:/PhD/prog_report_2025_June_project/data/Swiss/interim/simplified_edges.csv"
OUTPUT_XML = "D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss/simplified_network.edg.xml"
DELIMITER = ";"  # Corrected delimiter

# ──────────────────────────────────────────────────────────────────────────────
# Logging setup
# ──────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# ──────────────────────────────────────────────────────────────────────────────
# Main Function
# ──────────────────────────────────────────────────────────────────────────────
def main():
    logging.info(f"📥 Loading simplified edges from: {INPUT_CSV}")

    try:
        df = pd.read_csv(INPUT_CSV, delimiter=DELIMITER)
    except Exception as e:
        logging.error(f"❌ Failed to load input CSV: {e}")
        sys.exit(1)

    required_columns = {
        "edge_id", "from_stop_id", "to_stop_id", "geometry_wkt"
    }
    if not required_columns.issubset(set(col.strip() for col in df.columns)):
        logging.error(f"❌ Missing required columns: {required_columns}")
        sys.exit(1)

    logging.info(f"✅ Loaded {len(df)} simplified edge records")

    # Create XML structure
    edges_el = ET.Element("edges")

    for _, row in df.iterrows():
        edge_id = row["edge_id"]
        from_node = row["from_stop_id"]
        to_node = row["to_stop_id"]
        geometry = row["geometry_wkt"]

        edge_el = ET.SubElement(edges_el, "edge", {
            "id": edge_id,
            "from": from_node,
            "to": to_node,
            "priority": "1",
            "type": "rail",
            "shape": _wkt_to_shape(geometry)
        })

    # Save to XML
    tree = ET.ElementTree(edges_el)
    try:
        tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
        logging.info(f"✅ XML written successfully to: {OUTPUT_XML}")
    except Exception as e:
        logging.error(f"❌ Failed to write XML file: {e}")
        sys.exit(1)

# ──────────────────────────────────────────────────────────────────────────────
# Helper Function to Convert WKT to SUMO Shape Format
# ──────────────────────────────────────────────────────────────────────────────
def _wkt_to_shape(wkt_str):
    """
    Converts WKT LineString to SUMO-compatible shape string.

    Args:
        wkt_str (str): GeoJSON-style WKT string containing coordinates.

    Returns:
        str: A SUMO-compatible shape string (e.g. "x1,y1 x2,y2 x3,y3")
    """
    import json
    try:
        geojson = json.loads(wkt_str.replace("'", '"'))
        coords = geojson["coordinates"]
        shape_str = " ".join([f"{x},{y}" for x, y in coords])
        return shape_str
    except Exception as e:
        logging.warning(f"⚠️ Failed to parse shape: {e}")
        return ""

# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
