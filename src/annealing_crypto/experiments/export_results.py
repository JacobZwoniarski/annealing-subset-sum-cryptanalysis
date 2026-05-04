"""CSV export helpers for benchmark rows."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from pathlib import Path
from typing import Any


BENCHMARK_COLUMNS = (
    "scenario_id",
    "source",
    "n_bits",
    "trial",
    "seed",
    "solver",
    "success",
    "exact_hit",
    "objective_value",
    "runtime_ms",
    "hamming_distance",
    "target",
    "weight_sum",
    "evaluated_states",
    "num_reads",
    "num_sweeps",
)


def write_benchmark_csv(rows: Iterable[dict[str, Any]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=BENCHMARK_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({column: row.get(column, "") for column in BENCHMARK_COLUMNS})


def read_benchmark_csv(output_path: Path) -> list[dict[str, str]]:
    with output_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))
