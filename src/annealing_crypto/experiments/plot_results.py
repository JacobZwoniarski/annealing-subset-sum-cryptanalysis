"""Generate report-ready plots from benchmark CSV files."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def generate_benchmark_plots(input_csv: Path, output_dir: Path) -> list[Path]:
    data = pd.read_csv(input_csv)
    if data.empty:
        raise ValueError("benchmark CSV is empty")

    output_dir.mkdir(parents=True, exist_ok=True)
    data["success"] = data["success"].map(_to_bool)

    plot_specs = [
        (
            "success_rate_vs_n.png",
            "success",
            "mean",
            "Success rate",
            "Success rate",
        ),
        (
            "runtime_ms_vs_n.png",
            "runtime_ms",
            "mean",
            "Runtime [ms]",
            "Mean runtime [ms]",
        ),
        (
            "objective_value_vs_n.png",
            "objective_value",
            "median",
            "Best objective value",
            "Median objective value",
        ),
    ]

    outputs: list[Path] = []
    for filename, metric, aggregation, y_label, title in plot_specs:
        output_path = output_dir / filename
        _line_plot(data, metric, aggregation, y_label, title, output_path)
        outputs.append(output_path)
    return outputs


def _line_plot(
    data: pd.DataFrame,
    metric: str,
    aggregation: str,
    y_label: str,
    title: str,
    output_path: Path,
) -> None:
    grouped = (
        data.groupby(["source", "solver", "n_bits"], as_index=False)[metric]
        .agg(aggregation)
        .sort_values(["source", "solver", "n_bits"])
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    for (source, solver), series in grouped.groupby(["source", "solver"]):
        label = f"{source} / {solver}"
        ax.plot(series["n_bits"], series[metric], marker="o", label=label)

    ax.set_title(title)
    ax.set_xlabel("n bits")
    ax.set_ylabel(y_label)
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}
