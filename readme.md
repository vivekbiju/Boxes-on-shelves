<img width="1523" height="737" alt="image" src="https://github.com/user-attachments/assets/d82b296b-d44a-488f-8df5-c5f64862f871" />



# 📦 Boxes on Shelves: NSGA-II Optimizer

This project is a multi-objective optimization tool designed to arrange boxes of various sizes onto warehouse shelves. It uses the **NSGA-II (Non-dominated Sorting Genetic Algorithm II)** to find the best balance between maximizing space usage and maintaining a stable load distribution across shelves.

## 🚀 Features

* **Multi-Objective Optimization**: Simultaneously optimizes for **Space Utilization** (filling the bay) and **Load Balance** (even weight distribution).
* **Interactive Web Dashboard**: Built with **Streamlit** and **Plotly** for a modern, browser-based user experience.
* **3D Visualization**: Rotate, zoom, and inspect box placements in a fully interactive 3D environment.
* **Pareto Front Exploration**: Click through different optimal solutions to see how different trade-offs affect the physical layout.
* **Modular Architecture**: Cleanly separated into data models (`models.py`), optimization logic (`engine.py`), and the user interface (`app.py`).

## 🛠️ Project Structure

```text
/1-boxes-on-shelves/
├── app.py           # The Streamlit web application (Entry Point)
├── engine.py        # Core NSGA-II logic (Crossover, Mutation, Sorting)
├── models.py        # Data loading and physical validity checks
├── main.py          # Terminal-based version of the optimizer
├── requirements.txt # List of necessary Python libraries
└── data/            # Input data folder
    ├── products.txt # Product dimensions and quantities
    ├── baytp1.txt   # Overall bay dimensions
    └── shelves.txt  # Shelf positions and gap constraints

```

## 📋 Prerequisites

Ensure you have Python 3.8+ installed. You will also need to install the following dependencies:

```bash
pip install -r requirements.txt

```

*Required libraries: `pandas`, `numpy`, `plotly`, `streamlit`, `matplotlib`.*

## 🏃 How to Run

### Option 1: Web Dashboard (Recommended)

To launch the interactive dashboard, run the following command in your terminal:

```bash
streamlit run app.py

```

A new tab will automatically open in your default web browser.

### Option 2: Terminal Version

To run the optimization and see progress logs directly in your terminal:

```bash
python main.py

```

## ⚙️ How it Works

1. **Data Loading**: The system imports dimensions from the `data/` folder and converts units (mm to cm) for consistency.
2. **Initial Population**: A set of random, valid solutions is generated. Each solution ensures that boxes do not overlap and stay within shelf boundaries.
3. **Evolution**:
* **Selection**: Solutions are ranked based on their Pareto front position (dominance).
* **Crossover**: Parts of "good" solutions are combined to create new offspring.
* **Mutation**: Random changes (flipping boxes or shifting positions) are introduced to maintain diversity.


4. **Pareto Front**: The final output provides a range of "best" solutions, allowing the user to choose between high density or high stability.

---

*Developed as a high-performance logistics optimization tool.*
