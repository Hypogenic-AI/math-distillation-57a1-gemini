# Computational Tools for Equational Theories

## Main Repository: [equational_theories](equational_theories/)
This is the cloned repository of the Equational Theories Project by Terence Tao.

### Key Scripts
- `scripts/explain_implication.py`: Builds the implication graph from entries and explains paths.
- `scripts/find_dual.py`: Finds the dual of a given equation.
- `scripts/explore_magma.py`: Tools for testing magmas against laws.
- `scripts/generate_z3_counterexample.py`: Uses Z3 solver to find counterexamples to implications.
- `scripts/predictor/`: Contains the CNN model used to predict implications syntactically.

### Data
- `data/equations.txt`: The definitive list of all 4,694 equations studied.
- `data/2024-10-20-edge_list.csv.zip`: The resulting implication graph.
- `data/small_magma_examples.txt`: Examples of finite magmas that serve as counterexamples.

## Setup Instructions
The repository contains a `python_environment/` setup script. To use the scripts, ensure you have `networkx`, `json`, and `z3-solver` installed in your environment.
