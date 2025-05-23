import os
import logging
import pandas as pd
import ast

# ------------------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------------------------------------------
# File paths (LOCAL ONLY)
# ------------------------------------------------------------------------------
BASE_PATH = r"D:\PhD\prog_report_2025_June_project"
CLEAN_ROUTE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_fully_covered_by_sumo.csv")
SUMO_STOP_FILE = os.path.join(BASE_PATH, "data", "Swiss", "processed", "simpler_network", "simple_stops_edges_cleaned.csv")

# ------------------------------------------------------------------------------
# Diagnostic Script
# ------------------------------------------------------------------------------
def compare_abbreviations(route_file: str, sumo_file: str):
    """
    Compares stop abbreviations in the final clean route file vs SUMO network.

    Args:
        route_file (str): Path to cleaned train route file with stop abbreviation sequences.
        sumo_file (str): Path to the file with SUMO physical stop nodes and abbreviations.

    Returns:
        None
    """
    logging.info("🔍 Starting abbreviation diagnostic...")

    # --- Load routes ---
    try:
        df_routes = pd.read_csv(route_file, sep=';', encoding='utf-8')
        logging.info(f"✅ Loaded route file with shape: {df_routes.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load route file: {e}")
        return

    route_abbrs = set()
    for row in df_routes['stops']:
        try:
            stops = ast.literal_eval(row)
            route_abbrs.update([abbr.strip() for abbr in stops])
        except Exception:
            continue

    # --- Load SUMO stop node abbreviations ---
    try:
        df_sumo = pd.read_csv(sumo_file, sep=',', encoding='utf-8')
        logging.info(f"✅ Loaded SUMO stop node file with shape: {df_sumo.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load SUMO stop file: {e}")
        return

    if 'stop_abbr' not in df_sumo.columns:
        logging.error("❌ Column 'stop_abbr' not found in SUMO stop file.")
        return

    sumo_abbrs = set(df_sumo['stop_abbr'].dropna().astype(str).str.strip())

    # --- Comparison ---
    only_in_routes = route_abbrs - sumo_abbrs
    only_in_sumo = sumo_abbrs - route_abbrs
    common_abbrs = route_abbrs & sumo_abbrs

    logging.info("\n📊 Abbreviation Comparison Summary:")
    logging.info(f"  • Unique stop abbreviations in route file : {len(route_abbrs)}")
    logging.info(f"  • Unique stop abbreviations in SUMO file  : {len(sumo_abbrs)}")
    logging.info(f"  • Common abbreviations                    : {len(common_abbrs)}")
    logging.info(f"  • Abbr only in route file                : {len(only_in_routes)}")
    logging.info(f"  • Abbr only in SUMO file                 : {len(only_in_sumo)}")

    # Show samples
    print("\n🔍 Sample of abbreviations only in route file:")
    for abbr in list(only_in_routes)[:10]:
        print(f"  - {abbr}")

    print("\n🔍 Sample of abbreviations only in SUMO stop file:")
    for abbr in list(only_in_sumo)[:10]:
        print(f"  - {abbr}")

    print("\n✅ Diagnostic complete.")

# ------------------------------------------------------------------------------
# Run script
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    compare_abbreviations(CLEAN_ROUTE_FILE, SUMO_STOP_FILE)
