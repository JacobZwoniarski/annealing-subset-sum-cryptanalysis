"""Exhaustive subset-sum baseline for small instances."""

from __future__ import annotations

from itertools import product
from time import perf_counter

from annealing_crypto.subset_sum import SubsetSumInstance, objective_value
from annealing_crypto.types import SolverResult


def solve_brute_force(
    instance: SubsetSumInstance,
    *,
    max_bits: int = 24,
    stop_at_first_exact: bool = True,
) -> SolverResult:
    if instance.n_bits > max_bits:
        raise ValueError(
            f"brute force refused n_bits={instance.n_bits}; max_bits={max_bits}"
        )

    started_at = perf_counter()
    best_solution: tuple[int, ...] | None = None
    best_objective: int | None = None
    evaluated_states = 0

    for candidate in product((0, 1), repeat=instance.n_bits):
        evaluated_states += 1
        candidate_objective = objective_value(instance, candidate)
        if best_objective is None or candidate_objective < best_objective:
            best_solution = candidate
            best_objective = candidate_objective
            if stop_at_first_exact and candidate_objective == 0:
                break

    runtime_ms = (perf_counter() - started_at) * 1000
    assert best_solution is not None
    assert best_objective is not None

    return SolverResult(
        solver="brute_force",
        solution=best_solution,
        objective_value=best_objective,
        runtime_ms=runtime_ms,
        exact_hit=best_objective == 0,
        metadata={
            "evaluated_states": evaluated_states,
            "stop_at_first_exact": stop_at_first_exact,
            "max_bits": max_bits,
        },
    )
