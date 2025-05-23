"""
Script: generate_nodes_from_simple_stops.py

Description:
This script reads a CSV file (simple_stops_edges.csv) that maps logical station stops
to physical node IDs and WGS84 coordinates. It converts the coordinates to UTM format
and generates a SUMO-compatible .nod.xml file.

Additionally, it enriches the output by adding a 'Linie' column if available in a
secondary dataset (linie_mit_polygon.csv), allowing for future disambiguation of
multi-track stations.

Usage:
Ensure you have the following CSV files in your local environment:
    - simple_stops_edges.csv (columns: logical_stop_name, stop_abbr, physical_node_id, lat, lon)
    - linie_mit_polygon.csv (columns: START_OP, END_OP, Linie)

Output:
    - A .nod.xml file usable as input to SUMO network construction.
    - A cleaned and exploded CSV where each row is tied to a single Linie.

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
INPUT_SIMPLE_EDGES = r"D:/PhD/prog_report_2025_June_project/data/Swiss/processed/simpler_network/simple_stops_edges.csv"
INPUT_LINIE_POLYGON = r"D:/PhD/prog_report_2025_June_project/data/Swiss/raw/linie_mit_polygon.csv"
OUTPUT_NOD_XML = r"D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss/simple_stops.nod.xml"
OUTPUT_CSV_ENRICHED = r"D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss/simple_stops_edges_with_linie.csv"
OUTPUT_CSV_CLEANED = r"D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss/simple_stops_edges_cleaned.csv"

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

def generate_nodes():
    """
    Loads stop-to-node mapping, enriches it with 'Linie' column using START_OP/END_OP matching,
    converts coordinates to UTM, explodes Linie into individual rows, and writes a .nod.xml for SUMO.
    """
    logger.info("📥 Loading simple_stops_edges.csv...")
    try:
        df = pd.read_csv(INPUT_SIMPLE_EDGES)
    except Exception as e:
        logger.error(f"Failed to read input CSV: {e}")
        return

    logger.info("📥 Loading linie_mit_polygon.csv to extract Linie mappings...")
    try:
        df_linie = pd.read_csv(INPUT_LINIE_POLYGON, sep=';', dtype=str)
    except Exception as e:
        logger.error(f"Failed to read linie_mit_polygon.csv: {e}")
        return

    # Normalize columns to uppercase to ensure case-insensitive joins
    df['stop_abbr'] = df['stop_abbr'].str.upper()
    df_linie['START_OP'] = df_linie['START_OP'].str.upper()
    df_linie['END_OP'] = df_linie['END_OP'].str.upper()

    logger.info("🔗 Mapping Linie IDs to stop entries...")
    linie_map = df_linie[['START_OP', 'END_OP', 'Linie']].dropna().drop_duplicates()

    # For each stop_abbr in the simple CSV, collect all Linie values where it was used as START or END
    stop_to_linie = (
        pd.concat([
            linie_map[['START_OP', 'Linie']].rename(columns={'START_OP': 'stop_abbr'}),
            linie_map[['END_OP', 'Linie']].rename(columns={'END_OP': 'stop_abbr'})
        ])
        .drop_duplicates()
        .groupby('stop_abbr')['Linie']
        .apply(lambda x: ','.join(sorted(set(x))))
        .reset_index()
    )

    df = df.merge(stop_to_linie, on='stop_abbr', how='left')
    logger.info(f"✅ Linie values merged into simple_stops_edges.csv (non-null: {df['Linie'].notna().sum()})")

    logger.info("🧭 Converting WGS84 coordinates to UTM...")
    df[['x', 'y']] = df.apply(lambda row: pd.Series(convert_to_utm(row['lon'], row['lat'])), axis=1)

    logger.info(f"✍️ Writing enriched CSV to: {OUTPUT_CSV_ENRICHED}")
    df.to_csv(OUTPUT_CSV_ENRICHED, index=False)

    logger.info("🔄 Exploding Linie field to one row per Linie...")
    df_exploded = df.dropna(subset=['Linie']).copy()
    df_exploded['Linie'] = df_exploded['Linie'].astype(str)
    df_exploded = df_exploded.assign(
        Linie=df_exploded['Linie'].str.split(',')
    ).explode('Linie')

    df_exploded.to_csv(OUTPUT_CSV_CLEANED, index=False)
    logger.info(f"✅ Cleaned and exploded CSV saved to: {OUTPUT_CSV_CLEANED} with {len(df_exploded)} rows")

    logger.info("🧱 Creating .nod.xml for SUMO with unique nodes...")
    unique_nodes = df_exploded.drop_duplicates(subset=['physical_node_id', 'x', 'y'])
    nodes_elem = Element('nodes')
    for _, row in unique_nodes.iterrows():
        SubElement(nodes_elem, 'node', {
            'id': row['physical_node_id'],
            'x': str(row['x']),
            'y': str(row['y']),
            'type': 'priority'
        })

    try:
        ElementTree(nodes_elem).write(OUTPUT_NOD_XML, encoding='utf-8', xml_declaration=True)
        logger.info(f"📄 Node file written to: {OUTPUT_NOD_XML}")
    except Exception as e:
        logger.error(f"Failed to write .nod.xml file: {e}")
        return

    print("\n🎉 SUMO node file created successfully!")
    print(f"🧠 Total unique nodes: {len(unique_nodes)}")
    print(f"📁 Output file: {OUTPUT_NOD_XML}")

if __name__ == "__main__":
    generate_nodes()
