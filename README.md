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
uv sync --extra dev
uv run pytest
uv run annealing-crypto-demo
```

The LaTeX report will be prepared after the implementation and experiments are
stable.
