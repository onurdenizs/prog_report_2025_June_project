import os
import logging
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_csv(filepath, sep=';', encoding='utf-8'):
    """Load a CSV file with logging and error handling."""
    try:
        df = pd.read_csv(filepath, sep=sep, encoding=encoding)
        logging.info(f"✅ Loaded file: {filepath} with shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"❌ Failed to load file: {filepath}")
        raise e

def clean_stop_id(raw_stop_id):
    """Extract numeric part from a stop_id, e.g. '8503054:0:1' -> '8503054'."""
    return str(raw_stop_id).split(':')[0]

def enrich_and_filter_routes(routes_df, valid_stop_ids, stops_df, output_path):
    """
    Filter routes that contain only valid stop_ids and enrich with trip names.
    
    Args:
        routes_df (pd.DataFrame): DataFrame with trip_id and stops (list of stop_ids).
        valid_stop_ids (set): Set of stop_ids available in the SUMO network.
        stops_df (pd.DataFrame): Reference for mapping stop_id to logical names.
        output_path (str): Where to save the final enriched CSV.

    Returns:
        None
    """
    enriched_data = []

    for _, row in routes_df.iterrows():
        trip_id = row['trip_id']
        stop_sequence = row['stops']
        stop_sequence_clean = [clean_stop_id(sid) for sid in eval(stop_sequence)]  # eval used safely here

        # Filter out routes with any unknown stops
        if not set(stop_sequence_clean).issubset(valid_stop_ids):
            continue

        origin_id = stop_sequence_clean[0]
        dest_id = stop_sequence_clean[-1]

        try:
            origin_name = stops_df.loc[stops_df['stop_id'] == int(origin_id), 'logical_stop_name'].values[0]
            dest_name = stops_df.loc[stops_df['stop_id'] == int(dest_id), 'logical_stop_name'].values[0]
        except IndexError:
            continue  # Skip if either ID is not found in the mapping

        trip_name = f"{origin_name}-{dest_name}"
        enriched_data.append({'trip_id': trip_id, 'trip_name': trip_name, 'stops': stop_sequence_clean})

    result_df = pd.DataFrame(enriched_data)
    result_df.to_csv(output_path, sep=';', index=False)
    logging.info(f"💾 Saved {len(result_df)} filtered routes to: {output_path}")
    print(f"\n✅ Done! {len(result_df)} routes written to file.\n")

def main():
    logging.info("🚀 Starting route enrichment and filtering...")

    # Define paths
    base_path = "D:/PhD/prog_report_2025_June_project"
    condensed_path = os.path.join(base_path, "data/Swiss/interim/routes_condensed.csv")
    stop_map_path = os.path.join(base_path, "data/Swiss/interim/corrected_stops_with_mapping.csv")
    output_path = os.path.join(base_path, "data/Swiss/interim/routes_with_metadata.csv")

    # Load input files
    routes_df = load_csv(condensed_path, sep=';')
    stops_df = load_csv(stop_map_path, sep=';')

    # Prepare set of valid stop_ids for filtering
    valid_stop_ids = set(stops_df['stop_id'].astype(str).unique())

    enrich_and_filter_routes(routes_df, valid_stop_ids, stops_df, output_path)

if __name__ == "__main__":
    main()
