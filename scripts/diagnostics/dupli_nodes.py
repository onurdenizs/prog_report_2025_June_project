import pandas as pd

mapping = pd.read_csv("data/Swiss/interim/stop_mappings/stop_id_to_node_id.csv")
stop_times = pd.read_csv("data/Swiss/raw/gtfs/stop_times.txt")

trip_groups = stop_times.groupby("trip_id")
for trip_id, group in trip_groups:
    stop_ids = group.sort_values("stop_sequence")["stop_id"].tolist()
    node_ids = [mapping.set_index("stop_id").get("node_id").get(sid, None) for sid in stop_ids]
    unique_nodes = set(node_ids)
    if len(unique_nodes) == 1 and None not in unique_nodes:
        print(f"❗ Trip {trip_id} — All {len(stop_ids)} stops mapped to: {list(unique_nodes)[0]}")
        break
