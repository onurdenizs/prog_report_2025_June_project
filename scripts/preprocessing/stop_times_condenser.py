import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def extract_routes_condensed(input_path: str, output_path: str) -> None:
    """
    Extracts condensed route sequences from GTFS stop_times.txt by aggregating ordered stop_ids for each trip_id.

    Args:
        input_path (str): Path to the GTFS stop_times.txt file.
        output_path (str): Path to write the condensed output CSV with trip_id and stop_id sequence.
    """
    try:
        logging.info("🚀 Loading stop_times.txt...")
        df = pd.read_csv(input_path)
        logging.info(f"✅ File loaded: {input_path} with shape {df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load file: {e}")
        return

    try:
        logging.info("🔧 Cleaning stop_id values...")
        df['clean_stop_id'] = df['stop_id'].astype(str).str.split(':').str[0]

        logging.info("📐 Sorting and grouping stop sequences by trip_id...")
        df_sorted = df.sort_values(by=['trip_id', 'stop_sequence'])
        grouped = df_sorted.groupby('trip_id')['clean_stop_id'].apply(list).reset_index()
        grouped.columns = ['trip_id', 'stops']

        logging.info(f"💾 Saving condensed route data to: {output_path}")
        grouped.to_csv(output_path, sep=';', index=False)

        logging.info(f"🎉 Done! Saved {len(grouped)} unique trip routes.")
        print("\n🔍 Preview of saved routes_condensed.csv:")
        print(grouped.head(5).to_string(index=False))

    except Exception as e:
        logging.error(f"❌ Error during processing: {e}")

# === Run the Script ===

input_file = r"D:\PhD\prog_report_2025_June_project\data\Swiss\raw\gtfs\stop_times.txt"
output_file = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\routes_condensed.csv"

extract_routes_condensed(input_file, output_file)
