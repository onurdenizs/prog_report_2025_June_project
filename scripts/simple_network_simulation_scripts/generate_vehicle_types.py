# Filename: generate_vehicle_types.py

import pandas as pd
import logging
import os
from xml.etree.ElementTree import Element, SubElement, ElementTree
from xml.dom import minidom

# =============================
# CONFIGURATION
# =============================
ROLLMATERIAL_CSV = r"D:/PhD/prog_report_2025_June_project/data/Swiss/raw/rollmaterial.csv"
VEHICLE_TYPES_XML = r"D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss/vehicle_types.veh.xml"

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def sanitize_id(name: str) -> str:
    """Sanitize vehicle type names to be SUMO ID-compatible."""
    return name.strip().replace(" ", "_").replace("/", "_").replace("-", "_").replace("(", "").replace(")", "")

def write_pretty_xml(xml_element, output_path):
    """Write XML to file with pretty formatting using minidom."""
    rough_string = ElementTree(xml_element).write(output_path, encoding='utf-8', xml_declaration=True)
    dom = minidom.parse(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(dom.toprettyxml(indent="  "))

def generate_vehicle_types():
    """
    Parses the rollmaterial.csv, aggregates technical specifications by 'Vehicle type',
    and generates a SUMO-compatible vehicle type definition file (.veh.xml) with pretty formatting.
    """
    logger.info("📥 Loading vehicle specs from rollmaterial.csv...")
    try:
        df = pd.read_csv(ROLLMATERIAL_CSV, sep=';', low_memory=False)
    except Exception as e:
        logger.error(f"Failed to read input CSV: {e}")
        return

    logger.info(f"✅ Loaded {len(df)} rows. Grouping by 'Vehicle type'...")

    # Select and clean relevant fields
    columns = ['Vehicle type', 'Tare (empty weight)', 'Length over buffers', 'Operational Vmax in km/h']
    df_filtered = df[columns].dropna(subset=['Vehicle type'])

    grouped = (
        df_filtered.groupby('Vehicle type')
        .agg({
            'Tare (empty weight)': 'mean',
            'Length over buffers': 'mean',
            'Operational Vmax in km/h': 'mean'
        })
        .dropna()
    )

    logger.info(f"✅ Aggregated vehicle types: {len(grouped)} valid groups")

    logger.info("✍️ Writing SUMO vehicle type XML...")
    root = Element("vehicleTypes")

    for vtype, row in grouped.iterrows():
        vtype_id = sanitize_id(vtype)
        SubElement(root, "vType", {
            "id": vtype_id,
            "vClass": "rail",
            "accel": "0.5",
            "decel": "1.0",
            "length": f"{round(row['Length over buffers'], 2)}",
            "maxSpeed": f"{round(row['Operational Vmax in km/h'] / 3.6, 2)}",
            "sigma": "0",
            "minGap": "1.0",
            "guiShape": "rail"
        })

    try:
        write_pretty_xml(root, VEHICLE_TYPES_XML)
        logger.info(f"🎉 SUMO vehicle type file saved: {VEHICLE_TYPES_XML}")
        print(f"\n📦 Finished: {len(grouped)} vehicle types written to {VEHICLE_TYPES_XML}")
    except Exception as e:
        logger.error(f"❌ Failed to write vehicle types XML: {e}")

if __name__ == "__main__":
    generate_vehicle_types()
