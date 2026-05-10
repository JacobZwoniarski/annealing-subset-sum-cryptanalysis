"""Sanity checks for benchmark CSV files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from annealing_crypto.experiments.run_benchmark import BenchmarkConfig


@dataclass(frozen=True)
class ValidationReport:
    rows: int
    checks: tuple[str, ...]

    @property
    def ok(self) -> bool:
        return True

    def as_dict(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "rows": self.rows,
            "checks": list(self.checks),
        }


def validate_benchmark_csv(
    input_csv: Path,
    *,
    config: BenchmarkConfig | None = None,
) -> ValidationReport:
    data = pd.read_csv(input_csv)
    if data.empty:
        raise ValueError("benchmark CSV is empty")

    checks = [
        _check_required_columns(data),
        _check_objective_flags(data),
        _check_hamming_ranges(data),
        _check_runtime_ranges(data),
    ]
    if config is not None:
        checks.append(_check_expected_grid(data, config))

    return ValidationReport(rows=len(data), checks=tuple(checks))


def _check_required_columns(data: pd.DataFrame) -> str:
    required = {
        "scenario_id",
        "source",
        "n_bits",
        "trial",
        "seed",
        "solver",
        "success",
        "exact_hit",
        "known_solution_match",
        "objective_value",
        "runtime_ms",
        "hamming_distance",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"benchmark CSV is missing columns: {sorted(missing)}")
    return "required columns present"


def _check_objective_flags(data: pd.DataFrame) -> str:
    objective = pd.to_numeric(data["objective_value"], errors="coerce")
    if objective.isna().any():
        raise ValueError("objective_value contains missing or non-numeric values")
    if (objective < 0).any():
        raise ValueError("objective_value contains negative values")

    exact_hit = data["exact_hit"].map(_to_bool)
    success = data["success"].map(_to_bool)
    objective_zero = objective.abs() <= 1e-9
    if not (exact_hit == objective_zero).all():
        raise ValueError("exact_hit does not match objective_value == 0")
    if not (success == exact_hit).all():
        raise ValueError("success does not match exact_hit")
    return "exact-hit flags match objective values"


def _check_hamming_ranges(data: pd.DataFrame) -> str:
    hamming = pd.to_numeric(data["hamming_distance"], errors="coerce")
    if hamming.isna().any():
        raise ValueError("hamming_distance contains missing or non-numeric values")
    if ((hamming < 0) | (hamming > data["n_bits"])).any():
        raise ValueError("hamming_distance is outside [0, n_bits]")

    known_match = data["known_solution_match"].map(_to_bool)
    if not (known_match == (hamming == 0)).all():
        raise ValueError("known_solution_match does not match hamming_distance == 0")
    exact_hit = data["exact_hit"].map(_to_bool)
    if (known_match & ~exact_hit).any():
        raise ValueError("known_solution_match requires exact_hit")
    return "hamming distances and planted-vector flags are consistent"


def _check_runtime_ranges(data: pd.DataFrame) -> str:
    runtime = pd.to_numeric(data["runtime_ms"], errors="coerce")
    if runtime.isna().any():
        raise ValueError("runtime_ms contains missing or non-numeric values")
    if (runtime < 0).any():
        raise ValueError("runtime_ms contains negative values")
    return "runtime values are non-negative"


def _check_expected_grid(data: pd.DataFrame, config: BenchmarkConfig) -> str:
    expected_grid = {
        (source, size, trial, solver)
        for source in config.sources
        for size in config.sizes
        for trial in range(config.trials)
        for solver in config.solvers
    }
    expected_rows = len(expected_grid)

    expected_solvers = set(config.solvers)
    actual_solvers = set(data["solver"])
    if actual_solvers != expected_solvers:
        raise ValueError(f"solver set mismatch: expected {expected_solvers}, got {actual_solvers}")

    expected_sizes = set(config.sizes)
    actual_sizes = set(data["n_bits"])
    if actual_sizes != expected_sizes:
        raise ValueError(f"size set mismatch: expected {expected_sizes}, got {actual_sizes}")

    expected_sources = set(config.sources)
    actual_sources = set(data["source"])
    if actual_sources != expected_sources:
        raise ValueError(f"source set mismatch: expected {expected_sources}, got {actual_sources}")

    actual_counts = data.groupby(["source", "n_bits", "trial", "solver"]).size()
    duplicate_keys = actual_counts[actual_counts > 1]
    if not duplicate_keys.empty:
        raise ValueError(f"duplicate benchmark rows for {list(duplicate_keys.index)}")

    actual_grid = set(actual_counts.index)
    if actual_grid != expected_grid:
        missing = sorted(expected_grid - actual_grid)
        extra = sorted(actual_grid - expected_grid)
        raise ValueError(f"benchmark grid mismatch: missing={missing}, extra={extra}")

    if len(data) != expected_rows:
        raise ValueError(f"expected {expected_rows} rows, got {len(data)}")

    return "row count and benchmark grid match config"


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}
