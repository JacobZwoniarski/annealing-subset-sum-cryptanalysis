"""Aggregate benchmark CSV rows into compact report tables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


SUMMARY_COLUMNS = (
    "source",
    "solver",
    "n_bits",
    "trials",
    "exact_hit_rate",
    "known_solution_match_rate",
    "mean_runtime_ms",
    "median_runtime_ms",
    "median_objective_value",
    "mean_hamming_distance",
)


def summarize_benchmark(input_csv: Path) -> pd.DataFrame:
    data = pd.read_csv(input_csv)
    if data.empty:
        raise ValueError("benchmark CSV is empty")

    data["success"] = data["success"].map(_to_bool)
    data["exact_hit"] = data["exact_hit"].map(_to_bool)
    if "known_solution_match" in data:
        data["known_solution_match"] = data["known_solution_match"].map(_to_nullable_bool)
    else:
        data["known_solution_match"] = pd.NA

    summary = (
        data.groupby(["source", "solver", "n_bits"], as_index=False)
        .agg(
            trials=("scenario_id", "nunique"),
            exact_hit_rate=("exact_hit", "mean"),
            known_solution_match_rate=("known_solution_match", "mean"),
            mean_runtime_ms=("runtime_ms", "mean"),
            median_runtime_ms=("runtime_ms", "median"),
            median_objective_value=("objective_value", "median"),
            mean_hamming_distance=("hamming_distance", "mean"),
        )
        .sort_values(["source", "solver", "n_bits"])
    )
    return summary.loc[:, SUMMARY_COLUMNS]


def write_summary_csv(input_csv: Path, output_csv: Path) -> None:
    summary = summarize_benchmark(input_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_csv, index=False)


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def _to_nullable_bool(value: object) -> bool | None:
    if pd.isna(value) or str(value).strip() == "":
        return None
    return _to_bool(value)
