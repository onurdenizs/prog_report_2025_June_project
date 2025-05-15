import pandas as pd

file_path = "D:/PhD/prog_report_2025_June_project/data/Swiss/interim/simplified_edges.csv"

df = pd.read_csv(file_path, nrows=1)
print("🔍 Column names:")
for col in df.columns:
    print(f"- {col}")
