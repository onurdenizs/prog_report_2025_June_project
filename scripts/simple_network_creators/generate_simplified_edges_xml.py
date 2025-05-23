"""
Script: generate_edges_from_anchor_nodes.py

Description:
This script reads the cleaned stop-to-node mapping and line geometries,
matches anchor nodes for each segment, converts geo shapes to UTM,
and writes a SUMO-compatible .edg.xml file.

Input:
- edge_anchor_nodes.csv (Linie, START_OP, END_OP, START_NODE, END_NODE)
- linie_mit_polygon.csv (Linie, START_OP, END_OP, geo_shape)

Output:
- simplified_network.edg.xml (SUMO edge definitions with shapes)

Author: Onur Deniz
"""

import os
import logging
import pandas as pd
import json
from pyproj import Transformer
from xml.etree.ElementTree import Element, SubElement, ElementTree

# =============================
# CONFIGURATION
# =============================
INPUT_ANCHORS = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/edge_anchor_nodes.csv"
INPUT_POLYGONS = r"D:/PhD/prog_report_2025_June_project/data/Swiss/raw/linie_mit_polygon.csv"
OUTPUT_EDGES = r"D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss/simplified_network.edg.xml"

# Set up coordinate transformer (WGS84 -> UTM Zone 32N)
transformer = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def convert_linestring_to_utm(coords):
    """Convert a list of [lon, lat] pairs to UTM"""
    utm_coords = []
    for lon, lat in coords:
        x, y = transformer.transform(lon, lat)
        utm_coords.append(f"{round(x, 2)},{round(y, 2)}")
    return utm_coords

def generate_edges():
    logger.info("\U0001F4C5 Reading anchor and polygon datasets...")

    try:
        df_anchor = pd.read_csv(INPUT_ANCHORS, dtype=str)
        df_poly = pd.read_csv(INPUT_POLYGONS, sep=';', dtype=str)
    except Exception as e:
        logger.error(f"Failed to read input files: {e}")
        return

    # Preprocess
    df_poly = df_poly[['Linie', 'START_OP', 'END_OP', 'Geo shape']].dropna()
    df_poly['Linie'] = df_poly['Linie'].astype(str)

    # Merge datasets on Linie + endpoints
    logger.info("\U0001F501 Merging datasets on Linie, START_OP, END_OP...")
    df = pd.merge(df_poly, df_anchor, on=['Linie', 'START_OP', 'END_OP'], how='inner')
    logger.info(f"✅ Total segments to export: {len(df)}")

    # Start XML
    edges_elem = Element('edges')

    for _, row in df.iterrows():
        edge_id = f"{row['Linie']}_{row['START_NODE']}_{row['END_NODE']}"

        try:
            geo = json.loads(row['Geo shape'].replace("'", '"'))
            coords = geo.get('coordinates', [])

            # Fix cases where nested lists are returned
            if isinstance(coords[0][0], list):
                coords = coords[0]

            shape = convert_linestring_to_utm(coords)
            shape_str = " ".join(shape)

            SubElement(edges_elem, 'edge', {
                'id': edge_id,
                'from': row['START_NODE'],
                'to': row['END_NODE'],
                'priority': "1",
                'type': "rail",
                'shape': shape_str
            })
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse shape for {edge_id}: {e}")

    try:
        ElementTree(edges_elem).write(OUTPUT_EDGES, encoding='utf-8', xml_declaration=True)
        logger.info(f"📄 Edge file written to: {OUTPUT_EDGES}")
    except Exception as e:
        logger.error(f"❌ Failed to write .edg.xml file: {e}")
        return

if __name__ == "__main__":
    generate_edges()
