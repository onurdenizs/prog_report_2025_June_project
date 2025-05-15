"""
summarize_network_contents.py

Phase 6 of the SUMO Swiss Network Pipeline (April 2025 edition).
Parses the compiled .net.xml and reports key network metrics for validation.

Outputs:
    - Total number of nodes and edges
    - Junction types breakdown
    - Sample edge IDs and from-to connections

Input:
    - SUMO/input/april_2025_swiss.net.xml

Author: Onur Deniz
Date: 2025-05
"""

import os
import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd
import logging

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
INPUT_NET_PATH = "SUMO/input/april_2025_swiss.net.xml"

# ─────────────────────────────────────────────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    logging.info(f"📂 Phase 6: Validating network — {INPUT_NET_PATH}")

    if not os.path.exists(INPUT_NET_PATH):
        logging.error(f"❌ File not found: {INPUT_NET_PATH}")
        return

    try:
        tree = ET.parse(INPUT_NET_PATH)
        root = tree.getroot()
    except ET.ParseError as e:
        logging.error(f"❌ Failed to parse .net.xml: {e}")
        return

    nodes, edges = [], []

    for elem in root:
        if elem.tag == "junction":
            nodes.append(elem.attrib)
        elif elem.tag == "edge" and "id" in elem.attrib:
            edges.append(elem.attrib)

    df_nodes = pd.DataFrame(nodes)
    df_edges = pd.DataFrame(edges)

    # ─────────────────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────────────────
    logging.info("📊 Node Summary")
    logging.info(f"🔢 Total Nodes: {len(df_nodes):,}")
    if "type" in df_nodes.columns:
        junction_counts = dict(Counter(df_nodes["type"]))
        logging.info(f"📌 Junction Types: {junction_counts}")

    logging.info("📊 Edge Summary")
    logging.info(f"🔢 Total Edges: {len(df_edges):,}")

    if not df_edges.empty:
        edge_sample = df_edges["id"].sample(n=min(5, len(df_edges)), random_state=42).tolist()
        logging.info(f"🆔 Sample Edge IDs: {edge_sample}")

        if {"from", "to"}.issubset(df_edges.columns):
            logging.info("🔗 Sample from-to pairs:")
            sample_pairs = df_edges[["from", "to"]].dropna().sample(n=min(5, len(df_edges)), random_state=42)
            for _, row in sample_pairs.iterrows():
                logging.info(f"    ➜ {row['from']} → {row['to']}")

    logging.info("✅ Phase 6 complete. Network structure looks valid.")

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
