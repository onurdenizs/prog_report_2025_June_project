import os
import logging
import pandas as pd

# -----------------------------------------------------------------------------
# Logging configuration
# -----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------
def load_csv(filepath, sep=';', encoding='utf-8'):
    """
    Load a CSV file into a DataFrame with logging.

    Args:
        filepath (str): Path to the CSV file.
        sep (str): Separator character.
        encoding (str): File encoding.

    Returns:
        pd.DataFrame: Loaded DataFrame.
    """
    try:
        df = pd.read_csv(filepath, sep=sep, encoding=encoding)
        df.columns = df.columns.str.strip()  # Strip whitespace from column names
        logging.info(f"✅ Loaded file: {filepath} with shape: {df.shape}")
        return df
    except Exception as e:
        logging.error(f"❌ Failed to load file: {filepath}")
        raise e


def extract_train_number(trip_id):
    """
    Extract numeric train number from GTFS trip_id (prefix).
    
    Example: "24880.TA.91-XYZ" -> 24880

    Args:
        trip_id (str): Full trip_id string.

    Returns:
        int or None: Extracted numeric ID or None if not parseable.
    """
    try:
        return int(str(trip_id).split('.')[0])
    except Exception:
        return None


# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------
def main():
    logging.info("🚀 Starting to attach vehicle IDs to route metadata...")

    # File paths
    base_path = "D:/PhD/prog_report_2025_June_project"
    routes_path = os.path.join(base_path, "data/Swiss/interim/routes_with_metadata.csv")
    formation_path = os.path.join(base_path, "data/Swiss/raw/jahresformation.csv")
    mapping_path = os.path.join(base_path, "data/Swiss/raw/rollmaterial-matching.csv")
    output_path = os.path.join(base_path, "data/Swiss/interim/routes_and_vehicles_with_metadata.csv")

    # Load data
    routes_df = load_csv(routes_path)
    formation_df = load_csv(formation_path)
    mapping_df = load_csv(mapping_path)

    # Build lookup table: Train -> Block
    formation_lookup = formation_df.set_index('Train')['Block designation'].to_dict()

    # Build vehicle type mapping (block name to vehicle_id)
    mapping_df.columns = mapping_df.columns.str.strip()
    vehicle_map = mapping_df.set_index('Train scheduling')['Rolling stock'].to_dict()

    # Attach vehicle_id column
    enriched_rows = []
    found, not_found = 0, 0

    for _, row in routes_df.iterrows():
        trip_id = row['trip_id']
        train_number = extract_train_number(trip_id)

        vehicle_id = 'N/A'
        if train_number in formation_lookup:
            block = formation_lookup[train_number]
            if block in vehicle_map:
                vehicle_id = vehicle_map[block]
                found += 1
            else:
                not_found += 1
        else:
            not_found += 1

        enriched_rows.append({
            'trip_id': trip_id,
            'trip_name': row['trip_name'],
            'stops': row['stops'],
            'vehicle_id': vehicle_id
        })

    result_df = pd.DataFrame(enriched_rows)
    result_df.to_csv(output_path, sep=';', index=False)

    # Summary
    logging.info(f"📅 Routes enriched: {len(result_df)}")
    logging.info(f"🔍 Vehicle matches found: {found}")
    logging.info(f"⚠️ Routes with no vehicle match: {not_found}")
    logging.info(f"📂 Saved final file to: {output_path}\n")
    print(f"\n🚀 All done. {found} vehicle IDs matched, {not_found} unmatched.\n")


# -----------------------------------------------------------------------------
# Run
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
