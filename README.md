# Priority-Queue Based SAT Solver

This repository contains a Python implementation of a SAT solver developed during my Master's research. Unlike traditional CDCL solvers, this project explores a **Priority-Queue (PQ)** based approach to manage the search space and variable selection heuristics.

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

To run the solver on a specific instance:

```bash
python main2.py
```
To execute the batch runner for experiments:
```bash
python solver_batch_runner2.py
```
🔗 References
For a deep dive into the algorithmic design and logic flow, please refer to the Presentation Slides.