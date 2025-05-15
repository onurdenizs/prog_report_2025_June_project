"""
Script: generate_nodes_from_simple_stops.py

Description:
This script reads a CSV file (simple_stops_edges.csv) that maps logical station stops to physical node IDs and WGS84 coordinates.
It converts the coordinates to UTM format and generates a SUMO-compatible .nod.xml file.

Usage:
Ensure you have 'simple_stops_edges.csv' in your local environment with the expected columns:
    - logical_stop_name
    - stop_abbr
    - physical_node_id
    - lat
    - lon

Output:
A .nod.xml file that can be used as input to SUMO network construction.

Author: Onur Deniz
"""

import os
import logging
import pandas as pd
from pyproj import Transformer
from xml.etree.ElementTree import Element, SubElement, ElementTree

# =============================
# CONFIGURATION
# =============================
INPUT_CSV = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/simple_stops_edges.csv"
OUTPUT_NOD_XML = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/simple_stops.nod.xml"

# Set up coordinate transformer (WGS84 -> UTM Zone 32N)
transformer = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def convert_to_utm(lon: float, lat: float) -> tuple:
    """Convert WGS84 lat/lon to UTM (zone 32N)."""
    try:
        x, y = transformer.transform(lon, lat)
        return round(x, 2), round(y, 2)
    except Exception as e:
        logger.error(f"Coordinate conversion failed for ({lat}, {lon}): {e}")
        raise

def generate_nodes(input_csv: str, output_xml: str):
    """
    Reads a CSV with stop-node mappings and writes a .nod.xml file.

    Args:
        input_csv: Path to the input CSV file.
        output_xml: Path to the output SUMO .nod.xml file.
    """
    logger.info("📥 Loading stop-node mapping CSV...")
    try:
        df = pd.read_csv(input_csv)
    except Exception as e:
        logger.error(f"Failed to read input CSV: {e}")
        return

    required_cols = {'physical_node_id', 'lat', 'lon'}
    if not required_cols.issubset(df.columns):
        logger.error(f"Missing columns in CSV. Required: {required_cols}")
        return

    # Drop duplicates just in case
    df = df.drop_duplicates(subset=['physical_node_id'])
    logger.info(f"✅ Loaded {len(df)} unique nodes.")

    # Convert coordinates
    logger.info("🧭 Converting coordinates to UTM...")
    df[['x', 'y']] = df.apply(lambda row: pd.Series(convert_to_utm(row['lon'], row['lat'])), axis=1)

    # Create XML root
    nodes_elem = Element('nodes')

    for _, row in df.iterrows():
        SubElement(nodes_elem, 'node', {
            'id': row['physical_node_id'],
            'x': str(row['x']),
            'y': str(row['y']),
            'type': 'priority'
        })

    # Write XML
    try:
        ElementTree(nodes_elem).write(output_xml, encoding='utf-8', xml_declaration=True)
        logger.info(f"📄 Node file written to: {output_xml}")
    except Exception as e:
        logger.error(f"Failed to write .nod.xml file: {e}")
        return

    print("\n🎉 SUMO node file created successfully!")
    print(f"🧠 Total nodes: {len(df)}")
    print(f"📁 Output file: {output_xml}")

if __name__ == "__main__":
    generate_nodes(INPUT_CSV, OUTPUT_NOD_XML)
