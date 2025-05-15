import os
import logging
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from sklearn.neighbors import BallTree
import numpy as np

# ────────────────────────────────────────────────────────────────────────────────
# CONFIG
# ────────────────────────────────────────────────────────────────────────────────

STOP_NODE_MAPPING = "data/Swiss/interim/stop_mappings/stop_id_to_node_id.csv"
GTFS_STOPS = "data/Swiss/raw/gtfs/stops.txt"
HALTESTELLEN = "data/Swiss/raw/haltestellen_2025.csv"
OUTPUT_REFINED_MAPPING = "data/Swiss/interim/stop_mappings/stop_id_to_node_id_refined.csv"
OUTPUT_GEOJSON = "output/diagnostics/gtfs_stop_node_mapping_debug.geojson"
OUTPUT_CSV = "output/diagnostics/gtfs_stop_node_mapping_debug.csv"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ────────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ────────────────────────────────────────────────────────────────────────────────

logging.info("📥 Loading GTFS stops.txt...")
gtfs = pd.read_csv(GTFS_STOPS)
gtfs = gtfs.dropna(subset=["stop_lat", "stop_lon"])
gtfs["stop_lat"] = gtfs["stop_lat"].astype(float)
gtfs["stop_lon"] = gtfs["stop_lon"].astype(float)
gtfs["geometry"] = gtfs.apply(lambda row: Point(row["stop_lon"], row["stop_lat"]), axis=1)
gtfs_gdf = gpd.GeoDataFrame(gtfs, geometry="geometry", crs="EPSG:4326").to_crs(epsg=2056)

logging.info("📥 Loading stop-to-node mapping...")
mapping = pd.read_csv(STOP_NODE_MAPPING)

logging.info("📥 Loading haltestellen_2025.csv...")
halt = pd.read_csv(HALTESTELLEN)
halt = halt.rename(columns={"BPUIC": "stop_id"})
halt = halt.dropna(subset=["stop_id"])
halt["stop_id"] = halt["stop_id"].astype(str)

# ────────────────────────────────────────────────────────────────────────────────
# STEP 1 — REMOVE DUPLICATES BASED ON MINIMUM DISTANCE
# ────────────────────────────────────────────────────────────────────────────────

logging.info("🔍 Fixing duplicate stop_id entries in mapping...")
refined = mapping.sort_values("distance_m").drop_duplicates("stop_id", keep="first")
refined.to_csv(OUTPUT_REFINED_MAPPING, index=False)
logging.info(f"✅ Refined mapping saved to: {OUTPUT_REFINED_MAPPING}")

# ────────────────────────────────────────────────────────────────────────────────
# STEP 2 — CHECK MATCHES WITH HALTESTELLEN FILE
# ────────────────────────────────────────────────────────────────────────────────

merged = refined.merge(gtfs, on="stop_id", how="left")
merged["in_haltestellen"] = merged["stop_id"].isin(halt["stop_id"])
match_rate = merged["in_haltestellen"].mean() * 100
logging.info(f"📊 GTFS→Haltestellen Match Rate: {match_rate:.2f}%")

# ────────────────────────────────────────────────────────────────────────────────
# STEP 3 — DEBUG EXPORTS FOR VISUAL INSPECTION
# ────────────────────────────────────────────────────────────────────────────────

logging.info("🗺️ Exporting visual debug files...")
gdf_debug = gpd.GeoDataFrame(merged, geometry="geometry", crs="EPSG:2056")
gdf_debug.to_file(OUTPUT_GEOJSON, driver="GeoJSON")
gdf_debug.drop(columns="geometry").to_csv(OUTPUT_CSV, index=False)

logging.info(f"✅ GeoJSON exported to: {OUTPUT_GEOJSON}")
logging.info(f"✅ CSV exported to: {OUTPUT_CSV}")
logging.info("🎉 All done.")
