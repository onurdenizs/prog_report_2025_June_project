# quick_check_stop_coverage.py
import pandas as pd

gtfs_stops = pd.read_csv("data/Swiss/raw/gtfs/stop_times.txt")["stop_id"].nunique()
mapped_stops = pd.read_csv("data/Swiss/interim/stop_mappings/stop_id_to_node_id.csv")["stop_id"].nunique()

print(f"🧮 GTFS stop IDs in stop_times.txt:       {gtfs_stops:,}")
print(f"✅ Stops with mapped SUMO nodes:          {mapped_stops:,}")
print(f"📉 Coverage rate:                         {100 * mapped_stops / gtfs_stops:.2f}%")
