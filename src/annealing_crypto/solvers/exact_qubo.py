"""Exact BQM solver used only to validate tiny QUBO models."""

from __future__ import annotations

from time import perf_counter

import dimod

from annealing_crypto.qubo import build_subset_sum_bqm, sample_to_bits
from annealing_crypto.subset_sum import SubsetSumInstance
from annealing_crypto.types import SolverResult


def solve_exact_qubo(instance: SubsetSumInstance, *, max_bits: int = 20) -> SolverResult:
    if instance.n_bits > max_bits:
        raise ValueError(f"ExactSolver refused n_bits={instance.n_bits}; max_bits={max_bits}")

    bqm = build_subset_sum_bqm(instance)
    started_at = perf_counter()
    sampleset = dimod.ExactSolver().sample(bqm)
    best = sampleset.first
    runtime_ms = (perf_counter() - started_at) * 1000
    solution = sample_to_bits(best.sample, instance.n_bits)

    return SolverResult(
        solver="exact_qubo",
        solution=solution,
        objective_value=best.energy,
        runtime_ms=runtime_ms,
        exact_hit=best.energy == 0,
        metadata={
            "num_variables": instance.n_bits,
            "num_interactions": len(bqm.quadratic),
        },
    )
