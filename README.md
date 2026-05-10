# Annealing Subset-Sum Cryptanalysis

Educational Python project for modelling a toy Merkle-Hellman knapsack
cryptosystem as a subset-sum problem, encoding it as QUBO, and comparing exact
and annealing-based solvers.

The project is intentionally limited to small instances. It is a reproducible
demonstrator of cryptographic problem modelling, not a practical attack on
modern cryptographic systems.

## What Is Included

- toy Merkle-Hellman key generation, encryption, and trapdoor decryption,
- subset-sum instance generation from random and Merkle-Hellman sources,
- QUBO/BQM construction for the squared subset-sum residual,
- brute force, exact QUBO, simulated annealing, and local SQA-style solvers,
- benchmark export, validation, aggregation, and plot generation,
- a Jupyter notebook for inspecting the demo and benchmark outputs,
- the final report PDF in `report/`.

The SQA-style solver is a local classical simulation inspired by quantum
annealing. It is not a physical D-Wave QPU run.

## Repository Layout

```text
src/annealing_crypto/      Python package with models, solvers, CLI, experiments
tests/                     Unit and integration tests
notebooks/                 Demo and visualization notebook
experiments/configs/       Versioned benchmark configuration
experiments/raw/           Local generated benchmark CSV files, ignored by git
experiments/processed/     Local generated summaries, ignored by git
experiments/plots/         Local generated report plots, ignored by git
report/                    Final exported report PDF
```

## Reproduce The Project

Install dependencies:

```bash
uv sync --extra dev --extra notebook --no-editable
```

Run the test suite:

```bash
uv run --no-editable pytest
```

Run the demo CLI:

```bash
uv run --no-editable annealing-crypto-demo
```

Regenerate the report benchmark and plots:

```bash
uv run --no-editable annealing-crypto-benchmark --config experiments/configs/report_benchmark.json
uv run --no-sync annealing-crypto-validate --config experiments/configs/report_benchmark.json
uv run --no-editable annealing-crypto-summary
uv run --no-editable annealing-crypto-plots
```

Open the notebook:

```text
notebooks/01_demo_visualization.ipynb
```

Use the project interpreter from `.venv/bin/python` if VS Code asks for a
notebook kernel.

## Benchmark Notes

The report benchmark uses:

- sizes `8`, `12`, and `16`,
- `5` trials per setting,
- random and Merkle-Hellman-derived subset-sum instances,
- brute force, simulated annealing, and local SQA-style solvers.

The main metrics are:

- `exact_hit_rate`: whether the solver found any subset with objective value
  `0`,
- `known_solution_match_rate`: whether the recovered bit vector matches the
  planted vector,
- runtime, objective value, and Hamming distance.

Generated CSV files and plots are ignored by git so the repository stays small.
The final report PDF contains the selected plots and interpretation.

## Report

The final exported report is:

```text
report/Annealing_Subset_Sum_Cryptanalysis.pdf
```

The LaTeX source was prepared separately in Overleaf. Only the final PDF is
tracked in this repository.
