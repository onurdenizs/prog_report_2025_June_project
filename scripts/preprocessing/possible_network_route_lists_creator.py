import os
import logging
import pandas as pd
from ast import literal_eval

# ----------------------------------------------------------------------------
# Logging Configuration
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ----------------------------------------------------------------------------
# Utility Functions
# ----------------------------------------------------------------------------
def load_csv(path, sep=';', encoding='utf-8'):
    """
    Load a CSV file with error handling and logging.

    Args:
        path (str): File path.
        sep (str): CSV separator.
        encoding (str): File encoding.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        df = pd.read_csv(path, sep=sep, encoding=encoding, dtype=str)
        logging.info(f"✅ Loaded file: {path} with shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"❌ Failed to load file: {path}\n{e}")
        raise

# ----------------------------------------------------------------------------
# Route Enrichment Logic
# ----------------------------------------------------------------------------
def enrich_routes(routes_df, stop_map_df, matched_ids_set):
    """
    Filter and enrich routes with readable origin-destination names.

    Args:
        routes_df (pd.DataFrame): DataFrame with 'trip_id' and 'stops'.
        stop_map_df (pd.DataFrame): DataFrame with stop_id to name mapping.
        matched_ids_set (set): Set of valid stop IDs.

    Returns:
        (pd.DataFrame, int): Tuple of enriched DataFrame and count of discarded routes.
    """
    enriched_data = []
    discarded_count = 0

    # Build lookup dictionary for stop_id to name
    stop_map_df['number'] = stop_map_df['number'].astype(str).str.strip()
    stop_map_df['offizielle Haltestellen Bezeichnung'] = stop_map_df[
        'offizielle Haltestellen Bezeichnung'].astype(str).str.strip()
    stop_name_lookup = stop_map_df.set_index('number')[
        'offizielle Haltestellen Bezeichnung'].to_dict()

    for _, row in routes_df.iterrows():
        trip_id = row['trip_id']
        try:
            stop_list = literal_eval(row['stops'])
        except Exception as e:
            logging.warning(f"⚠️ Could not parse stops for trip {trip_id}: {e}")
            discarded_count += 1
            continue

        if not set(stop_list).issubset(matched_ids_set):
            discarded_count += 1
            continue

        origin_id, dest_id = stop_list[0], stop_list[-1]

        try:
            origin_name = stop_name_lookup[origin_id]
            dest_name = stop_name_lookup[dest_id]
        except KeyError:
            discarded_count += 1
            continue

        enriched_data.append({
            'trip_id': trip_id,
            'trip_name': f"{origin_name}-{dest_name}",
            'stops': stop_list
        })

    enriched_df = pd.DataFrame(enriched_data)
    return enriched_df, discarded_count

# ----------------------------------------------------------------------------
# Main Function
# ----------------------------------------------------------------------------
def main():
    logging.info("\U0001F680 Starting route metadata enrichment...")

    # File paths
    base_path = r"D:/PhD/prog_report_2025_June_project"
    ROUTES_PATH = os.path.join(base_path, "data/Swiss/interim/routes_condensed.csv")
    HALTESTELLE_PATH = os.path.join(base_path, "data/Swiss/raw/haltestelle-haltekante.csv")
    MATCHED_STOP_IDS_PATH = os.path.join(base_path, "data/Swiss/interim/matched_stop_ids.txt")
    OUTPUT_PATH = os.path.join(base_path, "data/Swiss/interim/routes_with_metadata.csv")

    # Load datasets
    routes_df = load_csv(ROUTES_PATH, sep=';')
    stop_map_df = load_csv(HALTESTELLE_PATH, sep=';')
    
    with open(MATCHED_STOP_IDS_PATH, 'r') as f:
        matched_ids = {line.strip() for line in f if line.strip()}
        logging.info(f"✅ Loaded {len(matched_ids)} matched stop IDs from {MATCHED_STOP_IDS_PATH}")

    # Enrich
    enriched_df, discarded = enrich_routes(routes_df, stop_map_df, matched_ids)
    enriched_df.to_csv(OUTPUT_PATH, sep=';', index=False)

    logging.info(f"\U0001F4BE Saved {len(enriched_df)} enriched routes to: {OUTPUT_PATH}")
    print(f"\n✅ Done! {len(enriched_df)} routes written to file. {discarded} routes were discarded.\n")

# ----------------------------------------------------------------------------
# Entry Point
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
