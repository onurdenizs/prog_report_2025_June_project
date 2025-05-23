"""
Script: generate_edges_from_polygon.py

Description:
Generates SUMO-compatible edge definitions using:
  - Geometries from linie_mit_polygon.csv
  - Anchor node mappings from edge_anchor_nodes.csv

Each railway segment is converted into one or more SUMO edges, named according to your scheme:
  - First edge: START_NODE
  - Last edge: END_NODE
  - Intermediate edges: {Linie}_{START_OP}_{END_OP}_<idx>

Output:
  - SUMO edge XML written to: data/Swiss/processed/simpler_network/simple_edges.edg.xml

Author: Onur Deniz
"""

import os
import logging
import pandas as pd
import json
from shapely.geometry import LineString
from xml.etree.ElementTree import Element, SubElement, ElementTree

# =============================
# CONFIGURATION
# =============================
POLYGON_CSV = r"D:/PhD/prog_report_2025_June_project/data/Swiss/raw/linie_mit_polygon.csv"
ANCHOR_CSV = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/edge_anchor_nodes.csv"
OUTPUT_EDGE_XML = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/simple_edges.edg.xml"

# =============================
# LOGGING
# =============================
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def parse_geometry(geo_str):
    try:
        geojson = json.loads(geo_str)
        return LineString(geojson["coordinates"])
    except Exception as e:
        logger.warning(f"Failed to parse geometry: {e}")
        return None

def generate_edges():
    logger.info("📥 Reading input files...")
    df_poly = pd.read_csv(POLYGON_CSV, sep=';', dtype=str)
    df_anchor = pd.read_csv(ANCHOR_CSV, dtype=str)

    df_poly['Linie'] = df_poly['Linie'].astype(str)
    df_anchor['Linie'] = df_anchor['Linie'].astype(str)

    edge_elem = Element('edges')
    edge_count = 0
    skipped = 0

    logger.info("🧠 Generating edge XML...")
    for _, row in df_poly.iterrows():
        linie = row['Linie']
        start_op = row['START_OP']
        end_op = row['END_OP']
        shape = parse_geometry(row['Geo shape'])

        if shape is None or len(shape.coords) < 2:
            skipped += 1
            continue

        match = df_anchor[(df_anchor['Linie'] == linie) &
                          (df_anchor['START_OP'] == start_op) &
                          (df_anchor['END_OP'] == end_op)]

        if match.empty:
            logger.warning(f"⚠️ No anchor match for {linie} {start_op}->{end_op}")
            skipped += 1
            continue

        start_node = match.iloc[0]['START_NODE']
        end_node = match.iloc[0]['END_NODE']

        coords = list(shape.coords)
        coord_count = len(coords)

        # First edge (start node)
        edge_id = start_node
        edge_shape = f"{coords[0][0]},{coords[0][1]} {coords[1][0]},{coords[1][1]}"
        SubElement(edge_elem, 'edge', {
            'id': edge_id,
            'from': start_node,
            'to': f"{linie}_{start_op}_{end_op}_1",
            'priority': '1',
            'type': 'rail',
            'shape': edge_shape
        })
        edge_count += 1

        # Intermediate edges
        for i in range(1, coord_count - 2):
            edge_id = f"{linie}_{start_op}_{end_op}_{i}"
            edge_shape = f"{coords[i][0]},{coords[i][1]} {coords[i+1][0]},{coords[i+1][1]}"
            SubElement(edge_elem, 'edge', {
                'id': edge_id,
                'from': f"{linie}_{start_op}_{end_op}_{i}",
                'to': f"{linie}_{start_op}_{end_op}_{i+1}",
                'priority': '1',
                'type': 'rail',
                'shape': edge_shape
            })
            edge_count += 1

        # Last edge (end node)
        last_intermediate = f"{linie}_{start_op}_{end_op}_{coord_count - 2}"
        edge_id = end_node
        edge_shape = f"{coords[-2][0]},{coords[-2][1]} {coords[-1][0]},{coords[-1][1]}"
        SubElement(edge_elem, 'edge', {
            'id': edge_id,
            'from': last_intermediate,
            'to': end_node,
            'priority': '1',
            'type': 'rail',
            'shape': edge_shape
        })
        edge_count += 1

    logger.info(f"✅ Edges written: {edge_count}")
    logger.info(f"⚠️ Skipped segments due to missing data: {skipped}")

    try:
        ElementTree(edge_elem).write(OUTPUT_EDGE_XML, encoding='utf-8', xml_declaration=True)
        logger.info(f"📄 SUMO edge XML saved to: {OUTPUT_EDGE_XML}")
    except Exception as e:
        logger.error(f"Failed to write edge XML: {e}")

if __name__ == "__main__":
    generate_edges()
