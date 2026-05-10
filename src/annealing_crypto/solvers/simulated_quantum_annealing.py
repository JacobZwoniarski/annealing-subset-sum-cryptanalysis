"""Local simulated quantum annealing-style solver."""

from __future__ import annotations

from math import exp, log, tanh
from random import Random
from time import perf_counter

from annealing_crypto.subset_sum import SubsetSumInstance, objective_value
from annealing_crypto.types import SolverResult


def solve_simulated_quantum_annealing(
    instance: SubsetSumInstance,
    *,
    num_reads: int = 50,
    num_sweeps: int = 300,
    trotter_slices: int = 8,
    beta: float = 0.05,
    transverse_field_start: float = 2.0,
    transverse_field_end: float = 0.02,
    seed: int | None = None,
) -> SolverResult:
    _validate_parameters(
        num_reads=num_reads,
        num_sweeps=num_sweeps,
        trotter_slices=trotter_slices,
        beta=beta,
        transverse_field_start=transverse_field_start,
        transverse_field_end=transverse_field_end,
    )

    rng = Random(seed)
    started_at = perf_counter()
    best_solution: tuple[int, ...] | None = None
    best_objective: int | None = None

    for _ in range(num_reads):
        replicas = [
            [rng.randint(0, 1) for _ in range(instance.n_bits)]
            for _ in range(trotter_slices)
        ]
        replica_objectives = [objective_value(instance, replica) for replica in replicas]

        for sweep in range(num_sweeps):
            gamma = _annealed_field(
                sweep=sweep,
                num_sweeps=num_sweeps,
                start=transverse_field_start,
                end=transverse_field_end,
            )
            coupling = _trotter_coupling(beta, gamma, trotter_slices)
            for slice_index in range(trotter_slices):
                bit_order = list(range(instance.n_bits))
                rng.shuffle(bit_order)
                for bit_index in bit_order:
                    _try_flip(
                        instance=instance,
                        replicas=replicas,
                        replica_objectives=replica_objectives,
                        slice_index=slice_index,
                        bit_index=bit_index,
                        coupling=coupling,
                        beta=beta,
                        rng=rng,
                    )

        for replica, replica_objective in zip(replicas, replica_objectives):
            if best_objective is None or replica_objective < best_objective:
                best_solution = tuple(replica)
                best_objective = replica_objective

    runtime_ms = (perf_counter() - started_at) * 1000
    assert best_solution is not None
    assert best_objective is not None

    return SolverResult(
        solver="simulated_quantum_annealing",
        solution=best_solution,
        objective_value=best_objective,
        runtime_ms=runtime_ms,
        exact_hit=best_objective == 0,
        metadata={
            "num_reads": num_reads,
            "num_sweeps": num_sweeps,
            "trotter_slices": trotter_slices,
            "beta": beta,
            "transverse_field_start": transverse_field_start,
            "transverse_field_end": transverse_field_end,
            "seed": seed,
        },
    )


def _try_flip(
    *,
    instance: SubsetSumInstance,
    replicas: list[list[int]],
    replica_objectives: list[int],
    slice_index: int,
    bit_index: int,
    coupling: float,
    beta: float,
    rng: Random,
) -> None:
    replica = replicas[slice_index]
    old_bit = replica[bit_index]
    old_objective = replica_objectives[slice_index]

    replica[bit_index] = 1 - old_bit
    new_objective = objective_value(instance, replica)
    problem_delta = beta * (new_objective - old_objective) / len(replicas)
    coupling_delta = _coupling_delta(replicas, slice_index, bit_index, old_bit, coupling)
    total_delta = problem_delta + coupling_delta

    if total_delta <= 0 or rng.random() < exp(-total_delta):
        replica_objectives[slice_index] = new_objective
        return

    replica[bit_index] = old_bit


def _coupling_delta(
    replicas: list[list[int]],
    slice_index: int,
    bit_index: int,
    old_bit: int,
    coupling: float,
) -> float:
    old_spin = _spin(old_bit)
    new_spin = -old_spin
    previous_spin = _spin(replicas[(slice_index - 1) % len(replicas)][bit_index])
    next_spin = _spin(replicas[(slice_index + 1) % len(replicas)][bit_index])
    neighbor_sum = previous_spin + next_spin
    return -coupling * new_spin * neighbor_sum + coupling * old_spin * neighbor_sum


def _spin(bit: int) -> int:
    return 1 if bit else -1


def _annealed_field(*, sweep: int, num_sweeps: int, start: float, end: float) -> float:
    if num_sweeps == 1:
        return end
    progress = sweep / (num_sweeps - 1)
    return start * (end / start) ** progress


def _trotter_coupling(beta: float, gamma: float, trotter_slices: int) -> float:
    argument = max(beta * gamma / trotter_slices, 1e-12)
    return -0.5 * log(tanh(argument))


def _validate_parameters(
    *,
    num_reads: int,
    num_sweeps: int,
    trotter_slices: int,
    beta: float,
    transverse_field_start: float,
    transverse_field_end: float,
) -> None:
    if num_reads <= 0:
        raise ValueError("num_reads must be positive")
    if num_sweeps <= 0:
        raise ValueError("num_sweeps must be positive")
    if trotter_slices <= 1:
        raise ValueError("trotter_slices must be greater than 1")
    if beta <= 0:
        raise ValueError("beta must be positive")
    if transverse_field_start <= 0 or transverse_field_end <= 0:
        raise ValueError("transverse fields must be positive")
    if transverse_field_end > transverse_field_start:
        raise ValueError("transverse_field_end must not exceed transverse_field_start")
