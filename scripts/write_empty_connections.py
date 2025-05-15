"""
write_empty_connections.py

Phase 4 of the SUMO Swiss Network Pipeline (April 2025 edition).
Creates an empty placeholder .con.xml file required for netconvert.

This file tells SUMO that no explicit internal connections are provided.
SUMO will automatically generate them during compilation.

Output:
    - SUMO/input/april_2025_swiss.con.xml

Author: Onur Deniz
Date: 2025-05
"""

import os
import logging
from xml.etree.ElementTree import Element, ElementTree

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
OUTPUT_PATH = "SUMO/input/april_2025_swiss.con.xml"

# ─────────────────────────────────────────────────────────────────────────────
# Logging setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    logging.info("🧱 Phase 4: Creating empty .con.xml file for SUMO...")

    try:
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        root = Element("connections")  # No children — SUMO will infer
        tree = ElementTree(root)
        tree.write(OUTPUT_PATH, encoding="UTF-8", xml_declaration=True)
        logging.info(f"💾 Saved: {OUTPUT_PATH}")
        logging.info("✅ Phase 4 complete. You're ready for Phase 5: netconvert.")
    except Exception as e:
        logging.error(f"❌ Failed to create .con.xml file: {e}")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
