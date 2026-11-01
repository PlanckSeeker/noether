# Noether

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%25style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type Checker: mypy](https://img.shields.io/badge/mypy-strict-blue.svg)](https://github.com/python/mypy)

**Noether** is a symbolic physics reasoning and plausibility engine operating as a Python eDSL (Embedded Domain-Specific Language) over SymPy. Rather than acting as a rigid binary compiler, Noether incorporates a **Kuhnian epistemic architecture** where physical equations are evaluated within explicit theoretical paradigms (`ParadigmContext`). Using an **Action Priority List (APL)**, it manages mathematical anomalies, order-of-magnitude approximations, and paradigm shifts dynamically.

---

## Key Features

* **$\mathbb{Q}^8$ SI Dimensional Lattice (`dimensions.py`):** Immutable dimensional analysis utilising exact rational arithmetic across 8 fundamental SI dimensions (Length, Mass, Time, Current, Temperature, Amount, LuminousIntensity, SolidAngle).
* **Kuhnian Epistemic APL (`priority_queue.py`, `patches.py`):** Evaluates mathematical expressions against paradigm constraints, applying symbolic patches (such as Small-Angle approximations and Asymptotic Term Drops) and tracking cumulative epistemic friction.
* **Projective Geometric Algebra (`algebra.py`):** Symbolic multivector engine for $\mathcal{G}_{3,0,1}$ supporting nilpotent basis elements ($e_0^2 = 0$).
* **Empirical Data Ingestion (`ingest.py`):** Native binding pipelines for CSV survey tables and astronomical FITS files.
* **PySide6 Visualizer (`ui/`):** A timeline UI featuring colour-coded epistemic events, dynamic error accumulation via the **Crisis Meter**, and crisp LaTeX rendering of SymPy AST snapshots using Matplotlib.

---

## Installation

Ensure you have **Python 3.12+** and **Poetry** or **Hatchling** installed. Clone the repository and install the package in editable mode with development dependencies:

```bash
git clone https://github.com/PlanckSeeker/noether.git
cd noether
pip install -e ".[dev]"
```

---

## Quick Start: Running the Demo

Noether comes with a pre-configured galactic rotation curve crisis scenario. You can launch the interactive PySide6 visualiser directly from your terminal using the console script entry point:

```bash
noether-log
```

Alternatively, you can run the demonstration script manually:

```bash
python examples/run_demo.py
```

---

## Running the Verification Suite

Noether features a comprehensive test suite covering dimensional fuzzing, patch validation, PGA algebra rules, and headless UI model slots using `pytest-qt`:

```bash
pytest -v
```

---

## Project Architecture

```text
noether/
├── pyproject.toml         # PEP 621 packaging & dependency configuration
├── README.md              # Project documentation
├── examples/              # Demonstration scripts (e.g., galactic rotation crisis)
├── src/
│   └── noether/
│       ├── core/          # Dimensions (Q8), Contexts (Fermi bounds), Algebra (PGA)
│       ├── apl/           # Epistemic state machine, Patches, Events
│       ├── data/          # CSV and FITS empirical ingesters
│       └── ui/            # PySide6 MainWindow, Timeline model, Delegate, Widgets
└── tests/                 # Pytest verification suites & conftest fixtures
```

---

## License

Distributed under the MIT License. See `LICENSE` for more information.