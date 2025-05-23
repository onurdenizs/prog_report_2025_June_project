"""
Script: generate_sumo_network.py

Description:
Runs netconvert to generate a SUMO .net.xml file using the prepared nodes and edges files.

Inputs:
- simple_stops.nod.xml: SUMO-compatible nodes
- simplified_network.edg.xml: SUMO-compatible edges

Output:
- simplified_network.net.xml: Final SUMO network file

Author: Onur Deniz
"""

import os
import subprocess
import logging

# ==========================
# CONFIGURATION
# ==========================
INPUT_DIR = r"D:/PhD/prog_report_2025_June_project/SUMO/input/simpler Swiss"
NODES_FILE = os.path.join(INPUT_DIR, "simple_stops.nod.xml")
EDGES_FILE = os.path.join(INPUT_DIR, "simplified_network.edg.xml")
OUTPUT_NET = os.path.join(INPUT_DIR, "simplified_network.net.xml")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def run_netconvert():
    """Runs the netconvert command to generate SUMO network from nodes and edges."""
    logger.info("🚀 Starting SUMO network generation via netconvert...")

    cmd = [
        "netconvert",
        f"--node-files={NODES_FILE}",
        f"--edge-files={EDGES_FILE}",
        f"--output-file={OUTPUT_NET}",
        "--geometry.remove",               # Optional cleanup of redundant geometry
        "--junctions.corner-detail=1",     # Simplify junction geometry
        "--verbose"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info("✅ Network generation completed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logger.error("❌ Netconvert failed.\n")
        print("--- NETCONVERT ERROR ---")
        print(e.stderr)

if __name__ == "__main__":
    run_netconvert()
