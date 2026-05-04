"""Run reproducible solver comparisons on subset-sum scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from annealing_crypto.config import DEFAULT_RANDOM_SEED
from annealing_crypto.experiments.scenarios import (
    BenchmarkScenario,
    ScenarioSource,
    build_instance,
    iter_scenarios,
)
from annealing_crypto.metrics import hamming_distance
from annealing_crypto.solvers.brute_force import solve_brute_force
from annealing_crypto.solvers.exact_qubo import solve_exact_qubo
from annealing_crypto.solvers.simulated_annealing import solve_simulated_annealing
from annealing_crypto.subset_sum import SubsetSumInstance
from annealing_crypto.types import SolverResult

SolverName = Literal["brute_force", "exact_qubo", "simulated_annealing"]


@dataclass(frozen=True)
class BenchmarkConfig:
    sizes: tuple[int, ...] = (8, 12, 16)
    trials: int = 5
    base_seed: int = DEFAULT_RANDOM_SEED
    sources: tuple[ScenarioSource, ...] = ("random", "merkle_hellman")
    solvers: tuple[SolverName, ...] = ("brute_force", "simulated_annealing")
    brute_force_max_bits: int = 24
    exact_qubo_max_bits: int = 18
    annealing_reads: int = 100
    annealing_sweeps: int = 1_000


def run_benchmark(config: BenchmarkConfig = BenchmarkConfig()) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    scenarios = iter_scenarios(
        sizes=config.sizes,
        trials=config.trials,
        base_seed=config.base_seed,
        sources=config.sources,
    )
    for scenario in scenarios:
        instance = build_instance(scenario)
        for solver in config.solvers:
            result = _run_solver(instance, solver, scenario, config)
            rows.append(_result_row(scenario, instance, result))
    return rows


def _run_solver(
    instance: SubsetSumInstance,
    solver: SolverName,
    scenario: BenchmarkScenario,
    config: BenchmarkConfig,
) -> SolverResult:
    if solver == "brute_force":
        return solve_brute_force(instance, max_bits=config.brute_force_max_bits)
    if solver == "exact_qubo":
        return solve_exact_qubo(instance, max_bits=config.exact_qubo_max_bits)
    if solver == "simulated_annealing":
        return solve_simulated_annealing(
            instance,
            num_reads=config.annealing_reads,
            num_sweeps=config.annealing_sweeps,
            seed=scenario.seed,
        )
    raise ValueError(f"unsupported solver: {solver}")


def _result_row(
    scenario: BenchmarkScenario,
    instance: SubsetSumInstance,
    result: SolverResult,
) -> dict[str, object]:
    distance = None
    success = result.exact_hit
    if instance.known_solution is not None:
        distance = hamming_distance(result.solution, instance.known_solution)
        success = distance == 0

    return {
        "scenario_id": scenario.scenario_id,
        "source": scenario.source,
        "n_bits": scenario.n_bits,
        "trial": scenario.trial,
        "seed": scenario.seed,
        "solver": result.solver,
        "success": success,
        "exact_hit": result.exact_hit,
        "objective_value": result.objective_value,
        "runtime_ms": result.runtime_ms,
        "hamming_distance": distance,
        "target": instance.target,
        "weight_sum": sum(instance.weights),
        "evaluated_states": result.metadata.get("evaluated_states"),
        "num_reads": result.metadata.get("num_reads"),
        "num_sweeps": result.metadata.get("num_sweeps"),
    }
