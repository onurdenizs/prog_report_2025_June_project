import os
import ast
import logging
import pandas as pd

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
BASE_PATH = r"D:\PhD\prog_report_2025_June_project"
ROUTE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_with_metadata_enhanced.csv")
HALTESTELLE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "raw", "haltestelle-haltekante.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_only_train.csv")

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------------------------------------------
# Filter Function
# ------------------------------------------------------------------------------
def filter_train_only_routes(route_file, haltestelle_file, output_file):
    """
    Filters the route file to include only routes where all stops are train stops.

    Args:
        route_file (str): Path to routes CSV with stop_id sequences.
        haltestelle_file (str): Path to haltestelle-haltekante.csv.
        output_file (str): Path to save the filtered routes.
    """
    logging.info("🔍 Starting filtering of routes to keep only train-related stops...")

    # Load route metadata
    try:
        routes_df = pd.read_csv(route_file, sep=';', encoding='utf-8')
        logging.info(f"✅ Loaded route file with shape: {routes_df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load route file: {e}")
        return

    # Load haltestelle and extract only TRAIN stop_ids
    try:
        halt_df = pd.read_csv(haltestelle_file, sep=';', dtype=str)
        logging.info(f"✅ Loaded haltestelle file with shape: {halt_df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load haltestelle file: {e}")
        return

    # Filter for TRAIN stops
    halt_df['meansOfTransport'] = halt_df['meansOfTransport'].str.upper().fillna('')
    train_stop_ids = set(halt_df[halt_df['meansOfTransport'] == "TRAIN"]['number'].dropna().astype(str))
    logging.info(f"✅ Identified {len(train_stop_ids)} TRAIN stop_ids from haltestelle")

    # Filter routes
    kept = []
    discarded = 0
    for _, row in routes_df.iterrows():
        try:
            stop_ids = ast.literal_eval(row['stops'])
            if all(str(sid).strip() in train_stop_ids for sid in stop_ids):
                kept.append(row)
            else:
                discarded += 1
        except Exception:
            discarded += 1

    filtered_df = pd.DataFrame(kept)
    try:
        filtered_df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        logging.info(f"💾 Saved filtered routes to: {output_file}")
    except Exception as e:
        logging.error(f"❌ Failed to save filtered file: {e}")
        return

    # Summary
    logging.info("\n📊 Route Filtering Summary:")
    logging.info(f"  • Total routes analyzed      : {len(routes_df)}")
    logging.info(f"  • Routes kept (train only)  : {len(filtered_df)}")
    logging.info(f"  • Routes discarded (non-train): {discarded}")
    logging.info("✅ Filtering complete.")

# ------------------------------------------------------------------------------
# Run Script
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    filter_train_only_routes(ROUTE_FILE, HALTESTELLE_FILE, OUTPUT_FILE)
