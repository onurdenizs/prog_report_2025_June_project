import os
import pandas as pd
import logging
import ast

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------
ROUTES_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\routes_with_metadata.csv"
OUTPUT_PATH = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\zurich_origin_routes.csv"

# ------------------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------------------------------------------------------------------
# Main logic
# ------------------------------------------------------------------------------
def main():
    logging.info("🔍 Loading routes_with_metadata.csv...")
    try:
        df = pd.read_csv(ROUTES_PATH, sep=';')
        logging.info(f"✅ Loaded file with shape: {df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load CSV file: {e}")
        return

    # Total number of routes
    total_routes = len(df)

    # Safely parse 'stops' column from string to list
    df['stops'] = df['stops'].apply(ast.literal_eval)

    # Find route with most stops
    df['num_stops'] = df['stops'].apply(len)
    max_row = df.loc[df['num_stops'].idxmax()]
    max_trip_id = max_row['trip_id']
    max_stop_count = max_row['num_stops']

    # Filter routes starting from Zürich HB
    zurich_df = df[df['trip_name'].str.startswith("Zürich HB-")].copy()

    # Save filtered result
    zurich_df.to_csv(OUTPUT_PATH, sep=';', index=False)
    logging.info(f"💾 Saved {len(zurich_df)} Zürich-origin routes to: {OUTPUT_PATH}")

    # Print results
    print("\n📊 Summary:")
    print(f"  • Total number of routes          : {total_routes}")
    print(f"  • Route with most stops           : {max_trip_id} ({max_stop_count} stops)")
    print(f"  • Zürich-origin routes saved      : {len(zurich_df)}\n")

# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
