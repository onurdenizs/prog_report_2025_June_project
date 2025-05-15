"""
parse_gtfs_to_route_edge_map.py

Parses GTFS stop_times and maps each trip_id to an ordered sequence of SUMO edge IDs,
based on shortest paths between matched SUMO nodes.

Outputs `route_edge_map.csv` for later use in .rou.xml generation.

Author: Onur Deniz
Date: 2025-05
"""

import os
import csv
import logging
import xml.etree.ElementTree as ET
import networkx as nx
import pandas as pd

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────

GTFS_DIR = "data/Swiss/raw/gtfs"
SUMO_NET_FILE = "SUMO/input/april_2025_swiss.net.xml"
NODE_MAPPING_FILE = "data/Swiss/interim/stop_mappings/stop_id_to_node_id_refined.csv"
OUTPUT_FILE = "data/Swiss/processed/routes/route_edge_map.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ────────────────────────────────────────────────────────────────────────────────
# LOAD SUMO NETWORK
# ────────────────────────────────────────────────────────────────────────────────

def load_sumo_network(net_file):
    logging.info("🔁 Loading SUMO network into directed graph...")
    tree = ET.parse(net_file)
    root = tree.getroot()

    G = nx.DiGraph()
    for edge in root.findall("edge"):
        if edge.get("function") == "internal":
            continue
        from_node = edge.get("from")
        to_node = edge.get("to")
        edge_id = edge.get("id")
        G.add_edge(from_node, to_node, id=edge_id)

    logging.info(f"✅ Loaded SUMO network with {G.number_of_nodes():,} nodes and {G.number_of_edges():,} edges.")
    sample_nodes = list(G.nodes)[:5]
    logging.info(f"🧪 Sample node IDs in SUMO graph: {sample_nodes}")
    return G

# ────────────────────────────────────────────────────────────────────────────────
# LOAD GTFS AND MAPPING
# ────────────────────────────────────────────────────────────────────────────────

def load_stop_sequences(gtfs_dir):
    logging.info("📅 Parsing GTFS stop_times.txt...")
    df = pd.read_csv(os.path.join(gtfs_dir, "stop_times.txt"))

    trip_to_stops = {}
    for trip_id, group in df.groupby("trip_id"):
        ordered_stops = (
            group.sort_values("stop_sequence")["stop_id"]
            .apply(lambda s: str(s).split(":")[0])  # strip suffix
            .tolist()
        )
        trip_to_stops[trip_id] = ordered_stops

    logging.info(f"✅ Found {len(trip_to_stops):,} unique trips in GTFS.")
    return trip_to_stops

def load_stop_node_mapping(mapping_file):
    logging.info("🔍 Loading stop-to-node mapping...")
    df = pd.read_csv(mapping_file)
    df["stop_id"] = df["stop_id"].astype(str).str.strip().str.split(":").str[0]
    mapping = dict(zip(df["stop_id"], df["node_id"]))
    logging.info(f"✅ Loaded {len(mapping):,} stop-node mappings.")
    return mapping

# ────────────────────────────────────────────────────────────────────────────────
# MAP TRIPS TO EDGE SEQUENCES
# ────────────────────────────────────────────────────────────────────────────────

def map_trips_to_edges(trip_to_stops, stop_node_map, sumo_graph):
    logging.info("🔧 Mapping trips to edge sequences...")
    trip_to_edges = {}
    total_trips = len(trip_to_stops)
    failed_trips = 0
    mapped_trips = 0

    for trip_id, stops in trip_to_stops.items():
        try:
            node_sequence = [stop_node_map[s] for s in stops if s in stop_node_map]
            if len(set(node_sequence)) < 2:
                failed_trips += 1
                continue

            full_edge_list = []
            success = True

            for i in range(len(node_sequence) - 1):
                try:
                    path = nx.shortest_path(sumo_graph, source=node_sequence[i], target=node_sequence[i + 1])
                    for u, v in zip(path[:-1], path[1:]):
                        edge_data = sumo_graph.get_edge_data(u, v)
                        if edge_data:
                            full_edge_list.append(edge_data['id'])
                except nx.NetworkXNoPath:
                    logging.debug(f"❌ Trip {trip_id}: No path between {node_sequence[i]} and {node_sequence[i + 1]}")
                    success = False
                    break

            if success and full_edge_list:
                trip_to_edges[trip_id] = full_edge_list
                mapped_trips += 1
            else:
                failed_trips += 1

        except Exception as e:
            logging.error(f"❌ Trip {trip_id}: Unexpected error: {e}")
            failed_trips += 1

    # Summary
    logging.info("\n📋 Mapping Summary")
    logging.info(f"• Total GTFS trips:         {total_trips:,}")
    logging.info(f"• Successfully mapped:      {mapped_trips:,}")
    logging.info(f"• Failed to map:            {failed_trips:,}")
    logging.info(f"• Coverage rate:            {100 * mapped_trips / total_trips:.2f}%\n")

    return trip_to_edges

# ────────────────────────────────────────────────────────────────────────────────
# EXPORT TO CSV
# ────────────────────────────────────────────────────────────────────────────────

def write_route_edge_map(output_path, trip_to_edges):
    logging.info(f"📂 Writing route-edge mappings to {output_path}...")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["trip_id", "edge_sequence"])
        for trip_id, edge_list in trip_to_edges.items():
            writer.writerow([trip_id, " ".join(edge_list)])
    logging.info("✅ route_edge_map.csv successfully written.")

# ────────────────────────────────────────────────────────────────────────────────
# MAIN
# ────────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sumo_graph = load_sumo_network(SUMO_NET_FILE)
    trip_to_stops = load_stop_sequences(GTFS_DIR)
    stop_node_map = load_stop_node_mapping(NODE_MAPPING_FILE)
    trip_to_edges = map_trips_to_edges(trip_to_stops, stop_node_map, sumo_graph)
    write_route_edge_map(OUTPUT_FILE, trip_to_edges)
