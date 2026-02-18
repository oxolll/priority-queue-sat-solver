# Priority-Queue Based SAT Solver

This repository contains a Python implementation of a SAT solver developed during my Master's research. Unlike traditional DPLL solvers, this project explores a **Priority-Queue (PQ)** based approach to manage the search space and variable selection heuristics.

## 📂 Project Structure

- **`solver2.py`**: The core solver logic. The implementation blocks in this file directly correspond to the architectural diagrams in `docs/pq_base.pptx`.
- **`main2.py`**: The main entry point for solving a single CNF instance.
- **`solver_batch_runner2.py`**: A utility script for running batch experiments across multiple benchmarks.
- **`docs/pq_base.pptx`**: Detailed presentation slides explaining the algorithm's flowchart and logic blocks.
- **`benchmarks/`**: Contains experimental results and test data (Excel/CSV formats).

## 🚀 Key Features

### 1. Priority-Queue Heuristics
Instead of a standard stack-based recursion, this solver uses a priority queue to dynamically determine the next variable assignment, aiming to guide the search towards potential solutions more effectively.

### 2. Unbounded Search (No $\tau$)
The algorithm is designed without a specific recursion depth limit ($\tau$). It performs an exhaustive search strategy guided by the priority queue until a satisfying assignment is found or unsatisfiability is proven.

### 3. Minimal Solution Search
Due to the specific assignment strategy and heuristics employed, the solver is biased towards finding **minimal solutions** (i.e., solutions where flipping any `True` variable to `False` would render the formula unsatisfied).

## 📊 Benchmark Data

The experimental data in the `benchmarks/` directory follows the SATLIB file naming convention:

* **Format**: `uf{vars}_{clauses}` or `uuf{vars}_{clauses}`
    * `uf`: Uniform Random 3-SAT, **Satisfiable** instances.
    * `uuf`: Uniform Random 3-SAT, **Unsatisfiable** instances.
* **Example**:
    * `uf20_91`: 20 variables, 91 clauses (Satisfiable).
    * `uuf50_218`: 50 variables, 218 clauses (Unsatisfiable).

## 🛠 Usage

### 1. Prepare Benchmarks
First, unzip the benchmark dataset:
```bash
unzip benchmarks.zip
```
### 2. Run Single Instance
To solve a specific SAT problem, run main2.py with the path to a .cnf file:
```bash
python main2.py benchmarks/uf20-01.cnf
```

### 3. Run Batch Experiments
To execute the batch runner for experiments:
```bash
python solver_batch_runner2.py
```
### 4. Configuration & Version Control
The core logic in solver2.py contains multiple iterations of the heuristic algorithm (e.g., v1, v2, v3).

Switching Versions: To use a different version, open solver2.py and comment/uncomment the corresponding code blocks in the execution section (Line 76~80 or 88).

Stop-at-First-Solution: Please note that only the latest version (v3.1) is configured to terminate immediately upon finding the first valid assignment (aiming for a solution). Older versions or specific configurations might continue searching the entire space or behave differently.

📈 Experimental Results
The repository provides two categories of experimental data:

1. General Benchmarks (General Experimental Results)
These files contain the overall performance metrics (time, decision counts) across standard SATLIB suites, comparing satisfiable (uf) and unsatisfiable (uuf) instances.

uf50-218: 50 variables, 218 clauses (Satisfiable) - See uf50_218_SAT.csv

uf75-325: 75 variables, 325 clauses (Satisfiable) - See uf75_325_SAT.csv

uuf50-218: 50 variables, 218 clauses (Unsatisfiable) - See uuf50_218_SAT.csv

2. Single Solution Models (Results Finding Only One Solution)
Specific logs focus on the solver's behavior when configured to stop immediately after finding the first satisfying assignment (v3.1 behavior). 

sols.csv: Contains the specific boolean assignments found for satisfiable instances.

H1v3.1.csv: Detailed metrics for the latest heuristic version (v3.1), which implements the "stop-at-first-solution" logic.

callcount.csv: Records the number of decisions made to reach the single solution.

🔗 References
For a deep dive into the algorithmic design and logic flow, please refer to the [Presentation Slides](https://github.com/oxolll/priority-queue-sat-solver/tree/main/docs).