"""
generate_net_with_netconvert.py

Phase 5 of the SUMO Swiss Network Pipeline (April 2025 edition).
Runs SUMO's netconvert to generate a compiled .net.xml file from
.nod.xml, .edg.xml, and .con.xml files.

Input:
    - SUMO/input/april_2025_swiss.nod.xml
    - SUMO/input/april_2025_swiss.edg.xml
    - SUMO/input/april_2025_swiss.con.xml

Output:
    - SUMO/input/april_2025_swiss.net.xml

Author: Onur Deniz
Date: 2025-05
"""

import os
import subprocess
import logging
import sys

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
SUMO_BIN = "netconvert"  # Ensure SUMO is on your system PATH
INPUT_DIR = "SUMO/input/"
OUTPUT_FILE = os.path.join(INPUT_DIR, "april_2025_swiss.net.xml")

# ─────────────────────────────────────────────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    logging.info("🔧 Phase 5: Compiling SUMO network using netconvert...")

    node_file = os.path.join(INPUT_DIR, "april_2025_swiss.nod.xml")
    edge_file = os.path.join(INPUT_DIR, "april_2025_swiss.edg.xml")
    con_file  = os.path.join(INPUT_DIR, "april_2025_swiss.con.xml")

    # Check input files exist
    for f in [node_file, edge_file, con_file]:
        if not os.path.exists(f):
            logging.error(f"❌ Required input missing: {f}")
            sys.exit(1)

    # Construct netconvert command
    cmd = [
        SUMO_BIN,
        f"--node-files={node_file}",
        f"--edge-files={edge_file}",
        f"--connection-files={con_file}",
        f"--output-file={OUTPUT_FILE}",
        "--no-turnarounds"
    ]

    logging.info("🔧 Executing netconvert command:")
    logging.info(" ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        if os.path.exists(OUTPUT_FILE):
            logging.info(f"✅ Network successfully compiled → {OUTPUT_FILE}")
            logging.info("🎉 Phase 5 complete. Ready for inspection or validation.")
        else:
            logging.error("❌ netconvert completed but .net.xml file was not created.")
    except subprocess.CalledProcessError:
        logging.error("❌ netconvert execution failed!", exc_info=True)

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
