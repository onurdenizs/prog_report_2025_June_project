# 🇨🇭 SUMO Swiss Network Simulation — June 2025 Progress Report

This project simulates realistic Swiss railway operations using [SUMO](https://www.eclipse.dev/sumo/) (Simulation of Urban MObility), with the ultimate goal of evaluating the feasibility and impact of **Virtual Coupling (VC)** in partially upgraded railway networks. It forms the core of a PhD thesis in Railway Engineering.

---

## 🎯 Project Objectives

- Build a simplified yet realistic rail network of Switzerland in SUMO
- Integrate real-world train schedules, stop mappings, and rolling stock specs
- Evaluate VC vs. non-VC operations based on KPIs (delays, headway, throughput)
- Support scalable routing and simulation pipelines in Python
- Publish academic results and use as a career portfolio

---

## 🧱 Project Structure

prog_report_2025_June_project/
│
├── data/ # [IGNORED] Raw/processed datasets (GTFS, vehicle specs, topologies)
├── output/ # [IGNORED] Figures, logs, route files
│
├── scripts/ # All SUMO + Python pipeline scripts
│ ├── dataset analysis/ # Analysis of input datasets
│ ├── preprocessing/ # Stop-edge mapping, filtering, cleaning
│ ├── diagnostics/ # Debug, validate, visualize
│ ├── simple_network_creators/
│ └── write_* # XML writers for nodes, edges, routes
│
├── SUMO/
│ ├── .gitkeep # Keeps folder structure in Git
│ └── input/ # SUMO network, vehicle types, route files (only non-large files)
│
├── Route Creation with GTFS Phase Details/
├── Route Creation with polygons/
├── create_project_structure.py
├── README.md
└── .gitignore


---

## 🔁 Core Workflow (Simplified)

1. **Extract & Convert Geometry** → `extract_nodes_and_edges.py`
2. **Write SUMO Nodes/Edges** → `write_sumo_nodes.py`, `write_sumo_edges.py`
3. **Generate SUMO Network** → `generate_net_with_netconvert.py`
4. **Map Stops to Nodes** → `generate_stop_node_mapping.py`
5. **Analyze & Merge Vehicles** → `merge_vehicle_data.py`
6. **Write Routes** → `parse_gtfs_to_route_edge_map.py`
7. **Visualize & Debug** → scripts in `/diagnostics/`

---

## 📚 Data Sources

- **GTFS**: SBB Switzerland public transport feeds (2025)
- **Formation Data**: `jahresformation.csv`
- **Rolling Stock**: `rollmaterial.csv`, `rollmaterial-matching.csv`
- **Topology**: `linie_mit_polygon.csv`, `haltestelle-haltekante.csv`

---

## 📌 Key Features

- UTM conversion for SUMO compatibility
- Multi-stop routing via edge-path inference
- Logical-to-physical stop mapping support
- Route validation and visual debugging
- Clean, modular code with logging and docstrings

---

## 🚫 Files Ignored by `.gitignore`

To keep the repository clean and under GitHub limits:

- `/data/`, `/output/`
- `/SUMO/input/gtfs_network/`
- All `.csv`, `.geojson`, `.log` files
- Temporary/backup files (`*.tmp`, `*.bak`, `~$*`)

---

## ✍️ Author

**Onur Deniz**  
Commercial Pilot ✈️ | PhD Candidate in Railway Engineering 🚆  
Working on Virtual Coupling and intelligent train control  
📍 Istanbul → Germany (Escape Plan™)

---

## 📄 License

[MIT License](LICENSE) *(add later if needed)*

---

Let me know if you’d like to:

- Split this into sections for GitHub Pages
- Add example outputs, diagrams, or results
- Prepare for eventual academic publication upload
