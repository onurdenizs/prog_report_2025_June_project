import os
import ast
import logging
import pandas as pd

# ------------------------------------------------------------------------------
# Logging setup
# ------------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ------------------------------------------------------------------------------
# File paths (LOCAL ONLY)
# ------------------------------------------------------------------------------
INPUT_FILE = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\routes_and_vehicles_only_train_abbr.csv"
OUTPUT_FILE = r"D:\PhD\prog_report_2025_June_project\data\Swiss\interim\routes_and_vehicles_only_train_abbr_clean.csv"

# ------------------------------------------------------------------------------
# Filtering Function
# ------------------------------------------------------------------------------
def filter_routes_without_unk(input_file, output_file):
    """
    Filters out routes that contain 'UNK' in their stop abbreviation list.

    Args:
        input_file (str): Path to the input CSV with stop abbreviation lists.
        output_file (str): Path to save the cleaned CSV.

    Returns:
        None
    """
    logging.info("🧹 Starting filtering of routes with 'UNK' stops...")

    try:
        df = pd.read_csv(input_file, sep=';', encoding='utf-8')
        logging.info(f"✅ Loaded route file with shape: {df.shape}")
    except Exception as e:
        logging.error(f"❌ Failed to load route file: {e}")
        return

    def is_valid_stop_list(stops_raw):
        try:
            stop_list = ast.literal_eval(stops_raw)
            return all(abbr != "UNK" for abbr in stop_list)
        except Exception:
            return False

    df_clean = df[df['stops'].apply(is_valid_stop_list)].copy()
    removed_count = len(df) - len(df_clean)

    try:
        df_clean.to_csv(output_file, sep=';', index=False, encoding='utf-8')
        logging.info(f"💾 Saved cleaned file to: {output_file}")
    except Exception as e:
        logging.error(f"❌ Failed to save cleaned output: {e}")
        return

    logging.info("\n📊 Filtering Summary:")
    logging.info(f"  • Original routes     : {len(df)}")
    logging.info(f"  • Clean routes kept   : {len(df_clean)}")
    logging.info(f"  • Routes removed      : {removed_count}")
    logging.info("✅ Filtering complete.")

# ------------------------------------------------------------------------------
# Execute
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    filter_routes_without_unk(INPUT_FILE, OUTPUT_FILE)
