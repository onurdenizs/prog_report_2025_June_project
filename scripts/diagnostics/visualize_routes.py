"""
visualize_routes.py

Visualizes random train routes from route_edge_map.csv on a 2D plot
using SUMO edge geometry data (from rail_edges_named.csv).

Handles both 2D and 3D WKT geometries (LINESTRING and LINESTRING Z).
Skips trips with missing or malformed edge sequences.

Author: Onur Deniz
Date: 2025-05
"""

import pandas as pd
import matplotlib.pyplot as plt
import random
import re
import os

# ────────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────────────────────────────────────

EDGE_GEOMETRY_FILE = "data/Swiss/processed/rail_edges_named.csv"
ROUTE_EDGE_MAP_FILE = "data/Swiss/processed/routes/route_edge_map.csv"
OUTPUT_FOLDER = "output/figures"
N_PLOTS = 5  # Number of random routes to plot
SAVE_PNG = True  # Set to True to save PNGs instead of only showing them

# ────────────────────────────────────────────────────────────────────────────────
# GEOMETRY PARSER
# ────────────────────────────────────────────────────────────────────────────────

MAX_WARNINGS = 10
parse_fail_count = 0

def parse_linestring(wkt_str):
    global parse_fail_count
    try:
        match = re.search(r"LINESTRING\s+Z?\s*\((.*?)\)", wkt_str)
        coords_str = match.group(1)
        coords = []
        for point in coords_str.split(","):
            parts = point.strip().split()
            if len(parts) >= 2:
                x, y = map(float, parts[:2])  # discard Z if present
                coords.append((x, y))
        return coords
    except Exception as e:
        parse_fail_count += 1
        if parse_fail_count <= MAX_WARNINGS:
            print(f"⚠️ Failed to parse geometry (#{parse_fail_count}): {wkt_str[:100]}... → {e}")
        return []

# ────────────────────────────────────────────────────────────────────────────────
# PLOTTING
# ────────────────────────────────────────────────────────────────────────────────

def plot_route(edge_sequence, trip_id, edge_coords_map, save_folder=None):
    plt.figure(figsize=(10, 6))
    for edge_id in edge_sequence:
        if edge_id in edge_coords_map:
            coords = edge_coords_map[edge_id]
            if coords:
                xs, ys = zip(*coords)
                plt.plot(xs, ys, linewidth=2)
    plt.title(f"Route for Trip ID: {trip_id}")
    plt.axis('equal')
    plt.grid(True)

    if save_folder:
        os.makedirs(save_folder, exist_ok=True)
        output_path = os.path.join(save_folder, f"{trip_id[:40]}.png")
        plt.savefig(output_path, dpi=200)
        print(f"✅ Saved plot for trip {trip_id} to: {output_path}")
        plt.close()
    else:
        plt.show()

# ────────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────────

def main():
    print("📥 Loading edge geometries...")
    edges_df = pd.read_csv(EDGE_GEOMETRY_FILE)
    routes_df = pd.read_csv(ROUTE_EDGE_MAP_FILE)

    edges_df = edges_df.dropna(subset=["geometry"])
    edges_df["edge_coords"] = edges_df["geometry"].apply(parse_linestring)
    edge_coords_map = dict(zip(edges_df["edge_id"], edges_df["edge_coords"]))

    sample = routes_df.sample(n=N_PLOTS)

    for _, row in sample.iterrows():
        trip_id = row["trip_id"]
        edge_seq_raw = row["edge_sequence"]
        if isinstance(edge_seq_raw, str) and edge_seq_raw.strip():
            edge_list = edge_seq_raw.split()
            plot_route(edge_list, trip_id, edge_coords_map, OUTPUT_FOLDER if SAVE_PNG else None)
        else:
            print(f"⚠️ Skipping trip {trip_id}: no valid edge sequence.")

if __name__ == "__main__":
    main()
