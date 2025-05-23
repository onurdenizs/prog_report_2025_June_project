import os
import ast
import logging
import pandas as pd

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------
BASE_PATH = "D:/PhD/prog_report_2025_June_project"
INPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_with_metadata.csv")
OUTPUT_FILE = os.path.join(BASE_PATH, "data", "Swiss", "interim", "routes_and_vehicles_with_metadata_enhanced.csv")

# ----------------------------------------------------------------------------
# Logging setup
# ----------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ----------------------------------------------------------------------------
# Enhancement Logic
# ----------------------------------------------------------------------------
def refine_vehicle_matches(input_path: str, output_path: str):
    """
    Enhance vehicle_id assignments in route metadata by checking for reversed routes.

    Args:
        input_path (str): Path to the original CSV file.
        output_path (str): Path to save the enhanced output.
    """
    logging.info("\U0001F680 Starting refinement of vehicle assignments based on full stop reversal...")

    # Load dataset
    df = pd.read_csv(input_path, sep=';', encoding='utf-8')

    # Ensure 'vehicle_id' column is string type and unify missing values
    df['vehicle_id'] = df['vehicle_id'].astype(str).replace({'nan': 'N/A', '': 'N/A'})

    # Create a dictionary to map stop sequences (as tuple) to vehicle_id
    stop_seq_to_vehicle = {}
    for _, row in df.iterrows():
        if row['vehicle_id'] != 'N/A':
            try:
                stops = tuple(ast.literal_eval(row['stops']))
                stop_seq_to_vehicle[stops] = row['vehicle_id']
            except Exception:
                continue

    # Enhance rows with no vehicle_id by checking for reversed stop sequences
    enhanced_count = 0
    new_vehicle_ids = []

    for _, row in df.iterrows():
        if row['vehicle_id'] != 'N/A':
            new_vehicle_ids.append(row['vehicle_id'])
            continue

        try:
            stops = tuple(ast.literal_eval(row['stops']))
            reversed_stops = tuple(reversed(stops))
            if reversed_stops in stop_seq_to_vehicle:
                new_vehicle_ids.append(stop_seq_to_vehicle[reversed_stops])
                enhanced_count += 1
            else:
                new_vehicle_ids.append('N/A')
        except Exception:
            new_vehicle_ids.append('N/A')

    df['vehicle_id'] = new_vehicle_ids
    df.to_csv(output_path, sep=';', index=False)

    # Logging summary
    total = len(df)
    filled = df[df['vehicle_id'] != 'N/A'].shape[0]
    unfilled = df[df['vehicle_id'] == 'N/A'].shape[0]

    logging.info("\n\U0001F4CA Enhancement Summary:")
    logging.info(f"  • Total routes                    : {total}")
    logging.info(f"  • Routes newly filled by reverse : {enhanced_count}")
    logging.info(f"  • Total routes with vehicle_id   : {filled}")
    logging.info(f"  • Remaining unassigned routes    : {unfilled}\n")
    logging.info("✅ Enhancement complete.")

# ----------------------------------------------------------------------------
# Execute
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    refine_vehicle_matches(INPUT_FILE, OUTPUT_FILE)
