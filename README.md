# 🚆 SUMO Swiss Network Simulation — June 2025 Project

This repository contains a structured simulation environment to model and evaluate **Swiss railway operations**, especially under **Virtual Coupling (VC)** scenarios, using [SUMO (Simulation of Urban Mobility)](https://www.eclipse.org/sumo/).

---

## 🎯 Purpose

This project supports a PhD thesis titled:

> **"Analysis of Virtual Coupling in Operations Through Railway Networks"**

The simulation models a partially VC-upgraded network, includes real Swiss train formations, and prepares the foundation for academic publications and professional use cases in transport engineering.

---

## 🗂 Project Structure


├── scripts/ # All core and diagnostic Python scripts
│ ├── dataset analysis/ # One-off analysis scripts for CSV files
│ ├── diagnostics/ # Coverage, validation, debugging
│ ├── simple_network_creators/ # Scripts for simplified SUMO networks
│ └── ... # Main simulation & GTFS processing scripts
├── SUMO/
│ ├── .gitkeep # Keeps folder tracked without large files
│ └── input/gtfs_network/ # (Ignored) Massive full-Switzerland GTFS network
├── data/ # 🚫 Ignored: Raw, interim, and processed datasets
├── output/ # 🚫 Ignored: Figures, logs, and visual outputs
├── reports/ # Optional: Markdown, LaTeX, or DOCX progress reports
└── .gitignore # Ignores large files and unneeded local data


---

## 🧪 Core Features

- ✔️ **Custom node and edge generation** using Swiss geo datasets (`linie_mit_polygon.csv`)
- ✔️ **GTFS integration** for route simulation and stop-edge mapping
- ✔️ **Realistic train vehicle types** from formation and technical data
- ✔️ **Diagnostics** to ensure route coverage and SUMO validity
- ✔️ **Modular pipeline** for rapid iteration, reusable for German networks

---

## ⚠️ GitHub Note

Large files over 100MB (e.g., full `april_2025_swiss.net.xml`) were **removed from history** to comply with GitHub limits. These are locally regenerated and ignored via `.gitignore`.

---

## 📚 Related Files

- `Progress Report JUNE 2025 Master Plan.docx` — main academic planning document
- `Generating Swiss Network Pipeline.docx` — technical documentation
- `DETAILED AI PROMPT.docx` — summarized project prompt for AI systems

---

## 📌 Future Goals

- Add `.rou.xml` route generators from GTFS + logic
- Implement VC fallback and failure cases
- Extend simulations to German rail networks

---

> _Maintained by [@onurdenizs](https://github.com/onurdenizs) — PhD Candidate, Railway Engineering_
