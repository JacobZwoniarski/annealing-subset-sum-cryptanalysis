# Annealing Subset-Sum Cryptanalysis

Educational Python project for modelling toy Merkle-Hellman cryptanalysis as
subset-sum, QUBO, and annealing problems.

Recommended repository name:

```text
annealing-subset-sum-cryptanalysis
```

## Scope

The project focuses on small educational instances, not practical attacks on
modern cryptographic systems.

Initial MVP:

- implement toy Merkle-Hellman key generation, encryption, and legal
  decryption,
- generate subset-sum attack instances,
- build the QUBO objective,
- compare brute force and simulated annealing solvers,
- export benchmark results and plots for the final report.

The reproducible benchmark uses brute force, exact QUBO solving, classical
simulated annealing, and a local simulated quantum annealing-style solver. It
does not claim results from a physical D-Wave QPU.

## Development

```bash
uv sync --extra dev --no-editable
uv run pytest
uv run annealing-crypto-demo
uv run --no-editable annealing-crypto-benchmark --config experiments/configs/report_benchmark.json
uv run --no-editable annealing-crypto-summary
uv run --no-editable annealing-crypto-plots
```

The demo notebook lives in `notebooks/01_demo_visualization.ipynb`. Generated
benchmark CSV files and plots are kept local under `experiments/` and are not
tracked by git.

The written report is developed separately in Overleaf. The final PDF should be
added under `report/` when it is ready.
