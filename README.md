# Annealing Subset-Sum Cryptanalysis

Educational Python project for modelling toy Merkle-Hellman cryptanalysis as
subset-sum, QUBO, and annealing problems.

Recommended repository name:

```text
annealing-subset-sum-cryptanalysis
```

## Scope

The project follows the plan in
`docs/subset_sum_merkle_hellman_qubo_plan.md`. It focuses on small educational
instances, not practical attacks on modern cryptographic systems.

Initial MVP:

- implement toy Merkle-Hellman key generation, encryption, and legal
  decryption,
- generate subset-sum attack instances,
- build the QUBO objective,
- compare brute force and simulated annealing solvers,
- export benchmark results and plots for the final report.

## Development

```bash
uv sync --extra dev --no-editable
uv run pytest
uv run annealing-crypto-demo
uv run --no-editable annealing-crypto-benchmark --sizes 8 12 --trials 3
uv run --no-editable annealing-crypto-summary
uv run --no-editable annealing-crypto-plots
```

The LaTeX report will be prepared after the implementation and experiments are
stable.

The demo notebook lives in `notebooks/01_demo_visualization.ipynb`. Generated
benchmark CSV files and plots are kept local under `experiments/` and are not
tracked by git.

The report scaffold is in `report/main.tex`. It intentionally stays lightweight
until the final experiment set is settled.
