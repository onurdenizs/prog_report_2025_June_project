import os
import ast
import logging
import pandas as pd

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
BASE_PATH = r"D:\PhD\prog_report_2025_June_project"
INPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_only_train.csv")
HALTESTELLE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "raw", "haltestelle-haltekante.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_only_train_abbr.csv")

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------------------------------------------------------------------
# Processing Logic
# ------------------------------------------------------------------------------
def enrich_with_abbreviations(route_file, haltestelle_file, output_file):
    """
    Replaces stop_ids in each route with their stop abbreviations based on haltestelle-haltekante.csv.

    Args:
        route_file (str): CSV with 'stops' column of stop_id lists.
        haltestelle_file (str): CSV with stop_id ↔ abbreviation mapping.
        output_file (str): File to save the updated output to.

    Returns:
        None
    """
    logging.info("🚀 Starting enhancement of stop_ids with abbreviations...")

    # Load route file
    try:
        df = pd.read_csv(route_file, sep=';', encoding='utf-8')
        logging.info(f"✅ Loaded route file: {route_file} with shape: {df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load route file: {e}")
        return

    # Load haltestelle
    try:
        halt_df = pd.read_csv(haltestelle_file, sep=';', dtype=str)
        logging.info(f"✅ Loaded haltestelle file: {haltestelle_file} with shape: {halt_df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load haltestelle file: {e}")
        return

    # Build mapping: stop_id → abbreviation
    halt_df['number'] = halt_df['number'].astype(str).str.strip()
    halt_df['abbreviation'] = halt_df['abbreviation'].fillna("UNK").str.strip()
    abbr_map = halt_df.set_index('number')['abbreviation'].to_dict()

    # Replace stop_ids with abbreviations
    enriched_stops = []
    total_processed = 0
    total_unmapped = 0

    for stops_raw in df['stops']:
        try:
            stop_ids = ast.literal_eval(stops_raw)
            abbrs = []
            for sid in stop_ids:
                sid_clean = str(sid).strip()
                abbr = abbr_map.get(sid_clean, "UNK")
                if abbr == "UNK":
                    total_unmapped += 1
                abbrs.append(abbr)
                total_processed += 1
            enriched_stops.append(abbrs)
        except Exception:
            enriched_stops.append(["UNK"])
            total_unmapped += 1

    df['stops'] = enriched_stops

    # Save
    try:
        df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        logging.info(f"💾 Saved enhanced file to: {output_file}")
    except Exception as e:
        logging.error(f"❌ Failed to save output: {e}")
        return

    # Final report
    logging.info("\n📊 Enhancement Summary:")
    logging.info(f"  • Total routes processed     : {len(df)}")
    logging.info(f"  • Total stop IDs processed  : {total_processed}")
    logging.info(f"  • Total unmapped stop IDs   : {total_unmapped}")
    logging.info("✅ Enhancement complete.")

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    enrich_with_abbreviations(INPUT_FILE, HALTESTELLE_FILE, OUTPUT_FILE)
