"""
analyze_route_edge_map_coverage.py

Analyzes coverage of GTFS trips in route_edge_map.csv.
Reports how many trips were successfully mapped vs. failed,
and why failures occurred.

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import os

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────

GTFS_TRIPS_FILE = "data/Swiss/raw/gtfs/trips.txt"
ROUTE_EDGE_MAP_FILE = "data/Swiss/processed/routes/route_edge_map.csv"
OUTPUT_FAILURES_FILE = "output/logs/unmapped_trips.csv"

# ────────────────────────────────────────────────────────────────────────────────
# ANALYSIS FUNCTION
# ────────────────────────────────────────────────────────────────────────────────

def analyze_mapping(gtfs_file, route_map_file, output_failures_file):
    print("📊 Analyzing route mapping coverage...")

    gtfs_df = pd.read_csv(gtfs_file)
    route_map_df = pd.read_csv(route_map_file)

    total_trips = len(gtfs_df)
    mapped_trips = 0
    failed_trips = []

    route_map_dict = dict(zip(route_map_df["trip_id"], route_map_df["edge_sequence"]))

    for trip_id in gtfs_df["trip_id"].unique():
        edge_seq = route_map_dict.get(trip_id, None)

        if edge_seq is None:
            reason = "❌ Not present in route_edge_map.csv"
        elif not isinstance(edge_seq, str) or not edge_seq.strip():
            reason = "⚠️ Empty or invalid edge sequence"
        else:
            mapped_trips += 1
            continue

        failed_trips.append({"trip_id": trip_id, "reason": reason})

    # Summary
    print("\n📋 Mapping Summary")
    print(f"• Total GTFS trips:         {total_trips:,}")
    print(f"• Successfully mapped:      {mapped_trips:,}")
    print(f"• Failed to map:            {len(failed_trips):,}")
    print(f"• Coverage rate:            {100 * mapped_trips / total_trips:.2f}%")

    # Save failure log
    if failed_trips:
        os.makedirs(os.path.dirname(output_failures_file), exist_ok=True)
        pd.DataFrame(failed_trips).to_csv(output_failures_file, index=False)
        print(f"\n🧾 Detailed failure list saved to: {output_failures_file}")

# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    analyze_mapping(GTFS_TRIPS_FILE, ROUTE_EDGE_MAP_FILE, OUTPUT_FAILURES_FILE)
