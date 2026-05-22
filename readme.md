
Live Demo: [boxes-on-shelves-app.streamlit.app](https://boxes-on-shelves-app.streamlit.app)


<img width="1523" height="737" alt="image" src="https://github.com/user-attachments/assets/d82b296b-d44a-488f-8df5-c5f64862f871" />




# 📦 Multi-Objective Shelf Packing Optimization Dashboard

An AI-driven 3D bin-packing and shelf-space optimization platform. This application leverages the **NSGA-II (Non-dominated Sorting Genetic Algorithm II)** metaheuristic to solve complex, multi-objective spatial layout problems—maximizing volumetric space utilization while minimizing structural load imbalances across shelving units.

The system features both a production-grade CLI pipeline for automated batch processing and an interactive Streamlit UI dashboard for real-time exploratory analysis.

---

## 🚀 Key Features

* **Multi-Objective Optimization (NSGA-II):** Simultaneously optimizes for conflicting metrics (Space Utilization vs. Shelf Load Variance) using customized genetic operators (crossover, phenotypic mutation, and fast non-dominated sorting).
* **3D Collision & Boundary Enforcement:** Uses Axis-Aligned Bounding Box (**AABB**) intersection logic to ensure realistic physical placement without structural overlap or margin violations.
* **Dual Execution Modes:**
  * **Interactive Dashboard:** Spin up a web app via Streamlit to tweak evolutionary hyper-parameters on the fly.
  * **Headless Script Pipeline:** Run headless programmatic configurations via a standard entry-point CLI script (`main.py`).
* **Interactive 3D Graphics:** Constructs high-fidelity 3D spatial representations using custom manual vertices, rendering interactive 6-faced bounding-box cuboids via Plotly `Mesh3D`.

---

## 📂 Project Architecture

```text
1-BOX-ON-SHELVES/
├── data/
│   ├── baytp1.txt             # Physical structural boundaries of the bay (mm converted to cm)
│   ├── products.txt           # Dimensions and quantities of items to pack
│   └── shelves.txt            # Placement positions and buffer gaps of shelves
├── app.py                     # Streamlit frontend web dashboard and state tracking
├── main.py                    # Independent CLI entry point script for automated optimization loops
├── engine.py                  # Core NSGA-II evolutionary logic (dominance sorting, operators)
├── models.py                  # Spatial validations, AABB collision engine, population initializers
├── utils.py                   # Plotly Mesh3D pipeline and 3D geometric matrix generation
├── requirements.txt           # Python ecosystem package dependencies
└── readme.md                  # System Documentation

```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd 1-BOX-ON-SHELVES

```

### 2. Configure Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🖥️ Usage

The codebase supports **two** entry methods depending on your workflow requirements:

### Method A: Streamlit UI Dashboard (Interactive)

```bash
streamlit run app.py

```

* Fine-tune evolutionary rates in the left sidebar panels.
* Compute and render a clickable Pareto front alongside an interactive 3D shelf visualizer.

### Method B: Standalone Script Pipeline (CLI Batch Processing)

```bash
python main.py

```

* Ideal for programmatic testing and embedding within larger backend services. Outputs generational statistics directly to the standard terminal stream.

---

## 🧬 Evolutionary Algorithmic Overview

### 1. Multi-Objective Formulation

The optimization vector targets two distinct dimensions:

* **Space Utilization ($f_1$):** Maximizes the total volume filled against total spatial capacity.

$$\text{Maximize } \frac{\sum V_{\text{product}}}{W_{\text{bay}} \times H_{\text{bay}} \times D_{\text{bay}}}$$


* **Load Balance ($f_2$):** Minimizes the structural variance ($\sigma$) of item distribution across shelves to safeguard physical balance.

$$\text{Minimize } \sigma(\mathbf{V}_{\text{shelves}})$$



### 2. Physical Constraints (AABB Collision System)

To guarantee real-world feasibility, every generated solution evaluates overlapping cuboid bounds across three coordinates:

```python
if (p['x'] < o['x'] + o['eff_width'] and p['x'] + ew > o['x'] and
    p['y'] < o['y'] + o['eff_height'] and p['y'] + eh > o['y'] and
    p['z'] < o['z'] + o['eff_length'] and p['z'] + el > o['z']):
    return False # Collision detected!

```

### 3. Evolutionary Pipeline

* **Selection:** Fast Non-Dominated Sorting groups populations into ranked Pareto fronts to manage multi-objective elitism.
* **Crossover:** Single-point genomic indexing on sequenced bounding-box positional arrays.
* **Mutation:** Phenotypic adjustments that either alter the orientation matrix ($90^\circ$ item rotation shifts) or apply directional nudges inside the container boundary.


