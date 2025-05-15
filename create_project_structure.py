import os

BASE_DIR = r"D:\PhD\prog_report_2025_June_project"

DIR_STRUCTURE = [
    "data/raw/swissTNE",
    "data/raw/gtfs",
    "data/raw/vehicles",
    "data/raw/mappings",
    "data/interim/nodes_edges",
    "data/interim/vehicle_enriched",
    "data/interim/stop_mappings",
    "data/interim/gtfs_routes",
    "data/processed/network",
    "data/processed/vehicle_types",
    "data/processed/routes",

    "scripts/network",
    "scripts/vehicles",
    "scripts/gtfs",
    "scripts/routing",
    "scripts/visualization",
    "scripts/utils",

    "config",

    "output/logs",
    "output/figures",
    "output/videos",

    "reports/progress_June2025",
    "reports/paper_drafts",

    "tests",

    "docs",
]

def create_directories(base_dir, subdirs):
    for subdir in subdirs:
        path = os.path.join(base_dir, subdir)
        os.makedirs(path, exist_ok=True)
        print(f"✅ Created: {path}")

if __name__ == "__main__":
    create_directories(BASE_DIR, DIR_STRUCTURE)
    print("\n🎉 All directories created successfully.")
