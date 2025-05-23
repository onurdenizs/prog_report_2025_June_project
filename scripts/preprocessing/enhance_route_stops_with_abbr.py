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
ROUTE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_with_metadata_enhanced.csv")
HALTEKANTE_FILE = os.path.join(BASE_PATH, "data", "Swiss", "raw", "haltestelle-haltekante.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_with_metadata_enhanced_V2.csv")

# ------------------------------------------------------------------------------
# Core processing function
# ------------------------------------------------------------------------------
def convert_stop_ids_to_abbr(route_file, haltekante_file, output_file):
    """
    Converts stop_id sequences in a route metadata file into official station abbreviations.

    Args:
        route_file (str): Path to the route file with stop_id sequences.
        haltekante_file (str): Path to haltestelle-haltekante.csv with stop_id and abbreviation.
        output_file (str): Where to save the new enriched file.

    Returns:
        None
    """
    logging.info("🚀 Starting conversion of stop_ids to stop abbreviations...")

    try:
        df = pd.read_csv(route_file, sep=';', encoding='utf-8')
        logging.info(f"✅ Loaded route file: {route_file} with shape: {df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load route file: {e}")
        return

    try:
        halte_df = pd.read_csv(haltekante_file, sep=';', encoding='utf-8', dtype=str)
        logging.info(f"✅ Loaded haltekante file: {haltekante_file} with shape: {halte_df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load haltekante file: {e}")
        return

    if 'number' not in halte_df.columns or 'abbreviation' not in halte_df.columns:
        logging.error("❌ haltekante file missing required columns: 'number' or 'abbreviation'")
        return

    # Create mapping: stop_id → abbreviation
    stop_map = halte_df.dropna(subset=['number', 'abbreviation']).drop_duplicates(subset='number')
    stop_map_dict = stop_map.set_index('number')['abbreviation'].to_dict()

    if len(stop_map_dict) < 100:
        logging.warning("⚠️ Warning: stop map seems suspiciously small.")

    enriched_stops = []
    unmapped_count = 0
    total_stops = 0

    for stops_raw in df['stops']:
        try:
            stop_ids = ast.literal_eval(stops_raw)
            abbrs = []
            for sid in stop_ids:
                total_stops += 1
                abbr = stop_map_dict.get(str(sid).strip(), "UNK")
                if abbr == "UNK":
                    unmapped_count += 1
                abbrs.append(abbr)
            enriched_stops.append(abbrs)
        except Exception:
            enriched_stops.append(["UNK"])
            unmapped_count += 1

    df['stops'] = enriched_stops

    try:
        df.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        logging.info(f"💾 Saved enriched file to: {output_file}")
    except Exception as e:
        logging.error(f"❌ Failed to save output: {e}")
        return

    logging.info("\n📊 Final Report:")
    logging.info(f"  • Total routes processed     : {len(df)}")
    logging.info(f"  • Total stop IDs processed  : {total_stops}")
    logging.info(f"  • Total unmapped stop IDs   : {unmapped_count}")
    logging.info("✅ Conversion complete.")

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    convert_stop_ids_to_abbr(ROUTE_FILE, HALTEKANTE_FILE, OUTPUT_FILE)
