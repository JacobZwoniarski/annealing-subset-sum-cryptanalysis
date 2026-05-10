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

Benchmark metrics separate two notions that matter in the report:

- `exact_hit_rate`: whether the solver found any subset with objective value
  `0`,
- `known_solution_match_rate`: whether it recovered the planted bit vector.

For random subset-sum instances these can differ, because multiple subsets may
produce the same target. The report benchmark uses a wider random weight range
to reduce accidental collisions. For Merkle-Hellman toy attacks, the planted
vector is the encrypted message, so both metrics are useful.

## Development

```bash
uv sync --extra dev --no-editable
uv run pytest
uv run annealing-crypto-demo
uv run --no-editable annealing-crypto-benchmark --config experiments/configs/report_benchmark.json
uv run --no-editable annealing-crypto-validate --config experiments/configs/report_benchmark.json
uv run --no-editable annealing-crypto-summary
uv run --no-editable annealing-crypto-plots
```

The demo notebook lives in `notebooks/01_demo_visualization.ipynb`. Generated
benchmark CSV files and plots are kept local under `experiments/` and are not
tracked by git.

The written report is developed separately in Overleaf. The final PDF should be
added under `report/` when it is ready.
