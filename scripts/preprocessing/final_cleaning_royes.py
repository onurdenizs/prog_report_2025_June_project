import os
import ast
import logging
import pandas as pd

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
ROUTE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_only_train_abbr_clean.csv")
SUMO_STOP_FILE = os.path.join(BASE_PATH, "data", "Swiss", "processed", "simpler_network", "simple_stops_edges_cleaned.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_fully_covered_by_sumo.csv")

# ------------------------------------------------------------------------------
# Filtering Logic
# ------------------------------------------------------------------------------
def filter_routes_covered_by_sumo():
    """
    Filters out routes that contain any stop abbreviation not represented in the SUMO network.
    """
    logging.info("🧹 Starting final route filtering using SUMO stop coverage...")

    # Load route file
    try:
        df_routes = pd.read_csv(ROUTE_FILE, sep=';', encoding='utf-8')
        logging.info(f"✅ Loaded route file with shape: {df_routes.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load route file: {e}")
        return

    # Load SUMO stop abbreviations
    try:
        df_sumo = pd.read_csv(SUMO_STOP_FILE, sep=',', encoding='utf-8')
        logging.info(f"✅ Loaded SUMO stop file with shape: {df_sumo.shape}")
        valid_abbrs = set(df_sumo['stop_abbr'].dropna().astype(str).str.strip())
    except Exception as e:
        logging.error(f"❌ Failed to load SUMO stop file: {e}")
        return

    # Filter out any route that contains unmatched stop_abbr
    valid_rows = []
    total_routes = len(df_routes)
    discarded = 0

    for _, row in df_routes.iterrows():
        try:
            stop_abbrs = ast.literal_eval(row['stops'])
            if all(abbr in valid_abbrs for abbr in stop_abbrs):
                valid_rows.append(row)
            else:
                discarded += 1
        except Exception:
            discarded += 1  # also discard malformed rows

    filtered_df = pd.DataFrame(valid_rows)

    # Save result
    try:
        filtered_df.to_csv(OUTPUT_FILE, sep=';', index=False, encoding='utf-8')
        logging.info(f"💾 Saved filtered routes to: {OUTPUT_FILE}")
    except Exception as e:
        logging.error(f"❌ Failed to save filtered routes: {e}")
        return

    # Report
    logging.info("\n📊 SUMO Route Coverage Filter Summary:")
    logging.info(f"  • Original routes         : {total_routes}")
    logging.info(f"  • Clean routes retained   : {len(filtered_df)}")
    logging.info(f"  • Routes removed          : {discarded}")
    logging.info("✅ Filtering complete.")

# ------------------------------------------------------------------------------
# Execute
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    filter_routes_covered_by_sumo()
