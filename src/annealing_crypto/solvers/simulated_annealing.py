"""Simulated annealing solver backed by dwave-neal."""

from __future__ import annotations

from time import perf_counter

import neal

from annealing_crypto.qubo import build_subset_sum_bqm, sample_to_bits
from annealing_crypto.subset_sum import SubsetSumInstance
from annealing_crypto.types import SolverResult


def solve_simulated_annealing(
    instance: SubsetSumInstance,
    *,
    num_reads: int = 100,
    num_sweeps: int = 1_000,
    seed: int | None = None,
) -> SolverResult:
    if num_reads <= 0:
        raise ValueError("num_reads must be positive")
    if num_sweeps <= 0:
        raise ValueError("num_sweeps must be positive")

    bqm = build_subset_sum_bqm(instance)
    sampler = neal.SimulatedAnnealingSampler()
    started_at = perf_counter()
    sampleset = sampler.sample(
        bqm,
        num_reads=num_reads,
        num_sweeps=num_sweeps,
        seed=seed,
    )
    best = sampleset.first
    runtime_ms = (perf_counter() - started_at) * 1000
    solution = sample_to_bits(best.sample, instance.n_bits)

    return SolverResult(
        solver="simulated_annealing",
        solution=solution,
        objective_value=best.energy,
        runtime_ms=runtime_ms,
        exact_hit=best.energy == 0,
        metadata={
            "num_reads": num_reads,
            "num_sweeps": num_sweeps,
            "seed": seed,
            "num_variables": instance.n_bits,
        },
    )
