"""Aggregate benchmark CSV rows into compact report tables."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


SUMMARY_COLUMNS = (
    "source",
    "solver",
    "n_bits",
    "trials",
    "success_rate",
    "mean_runtime_ms",
    "median_objective_value",
    "mean_hamming_distance",
)


def summarize_benchmark(input_csv: Path) -> pd.DataFrame:
    data = pd.read_csv(input_csv)
    if data.empty:
        raise ValueError("benchmark CSV is empty")

    data["success"] = data["success"].map(_to_bool)
    summary = (
        data.groupby(["source", "solver", "n_bits"], as_index=False)
        .agg(
            trials=("scenario_id", "nunique"),
            success_rate=("success", "mean"),
            mean_runtime_ms=("runtime_ms", "mean"),
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
