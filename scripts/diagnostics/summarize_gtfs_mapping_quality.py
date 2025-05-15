"""
summarize_gtfs_mapping_quality.py

Checks consistency and coverage of GTFS stop_id → SUMO node_id mappings by comparing:
- GTFS stops.txt
- stop_id_to_node_id.csv
- haltestellen_2025.csv

Author: Onur Deniz
Date: 2025-05
"""

import os
import pandas as pd
import logging

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
GTFS_STOP_FILE = os.path.join(PROJECT_ROOT, "..", "..", "data", "Swiss", "raw", "gtfs", "stops.txt")
STOP_NODE_MAPPING_FILE = os.path.join(PROJECT_ROOT, "..", "..", "data", "Swiss", "interim", "stop_mappings", "stop_id_to_node_id.csv")
HALTESTELLEN_FILE = os.path.join(PROJECT_ROOT, "..", "..", "data", "Swiss", "raw", "haltestellen_2025.csv")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ────────────────────────────────────────────────────────────────────────────────
# LOAD FILES
# ────────────────────────────────────────────────────────────────────────────────

def load_datasets():
    logging.info("📥 Loading GTFS stops.txt...")
    gtfs_df = pd.read_csv(GTFS_STOP_FILE, dtype=str)
    logging.info(f"✅ Loaded {len(gtfs_df):,} GTFS stops.")

    logging.info("📥 Loading stop-to-node mapping...")
    mapping_df = pd.read_csv(STOP_NODE_MAPPING_FILE, dtype=str)
    logging.info(f"✅ Loaded {len(mapping_df):,} stop-node mappings.")

    logging.info("📥 Loading haltestellen_2025.csv...")
    halt_df = pd.read_csv(HALTESTELLEN_FILE, dtype=str)
    logging.info(f"✅ Loaded {len(halt_df):,} haltestellen records.")

    return gtfs_df, mapping_df, halt_df

# ────────────────────────────────────────────────────────────────────────────────
# DIAGNOSTICS
# ────────────────────────────────────────────────────────────────────────────────

def run_diagnostics(gtfs_df, mapping_df, halt_df):
    logging.info("\n🔎 Running Diagnostics...\n")

    # 1. Coverage check
    gtfs_stop_ids = set(gtfs_df["stop_id"].str.strip())
    mapped_stop_ids = set(mapping_df["stop_id"].str.strip())
    halt_stop_ids = set(halt_df["BPUIC"].str.strip())

    coverage = len(mapped_stop_ids & gtfs_stop_ids) / len(gtfs_stop_ids) * 100
    extra_in_mapping = mapped_stop_ids - gtfs_stop_ids
    missing_in_mapping = gtfs_stop_ids - mapped_stop_ids

    # 2. Duplicate node_ids
    duplicate_nodes = mapping_df["node_id"].value_counts()
    duplicate_nodes = duplicate_nodes[duplicate_nodes > 1]

    # 3. Unmatched with haltestellen
    missing_in_halt = gtfs_stop_ids - halt_stop_ids
    halt_coverage = len(gtfs_stop_ids & halt_stop_ids) / len(gtfs_stop_ids) * 100

    # 4. Diagnostic log
    logging.info("📊 Mapping Quality Summary")
    logging.info(f"• GTFS total stops:              {len(gtfs_stop_ids):,}")
    logging.info(f"• Successfully mapped to node:  {len(mapped_stop_ids & gtfs_stop_ids):,}")
    logging.info(f"• Missing from mapping:         {len(missing_in_mapping):,}")
    logging.info(f"• Extra in mapping:             {len(extra_in_mapping):,}")
    logging.info(f"• Duplicate node_ids used:      {len(duplicate_nodes):,}")
    logging.info(f"• GTFS stops matched in halt:   {len(gtfs_stop_ids & halt_stop_ids):,}")
    logging.info(f"• GTFS stops NOT in halt:       {len(missing_in_halt):,}")
    logging.info(f"• 🔍 GTFS→Node Coverage:         {coverage:.2f}%")
    logging.info(f"• 🔍 GTFS→Haltestellen Match:    {halt_coverage:.2f}%")

    # Optionally save problem lists
    mismatch_dir = os.path.join(PROJECT_ROOT, "..", "..", "output", "diagnostics")
    os.makedirs(mismatch_dir, exist_ok=True)

    pd.Series(sorted(missing_in_mapping)).to_csv(os.path.join(mismatch_dir, "missing_in_mapping.csv"), index=False)
    pd.Series(sorted(missing_in_halt)).to_csv(os.path.join(mismatch_dir, "missing_in_haltestellen.csv"), index=False)
    duplicate_nodes.to_csv(os.path.join(mismatch_dir, "duplicate_node_ids.csv"))

    logging.info("📁 Problem lists saved in: output/diagnostics/")

# ────────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    gtfs_df, mapping_df, halt_df = load_datasets()
    run_diagnostics(gtfs_df, mapping_df, halt_df)
