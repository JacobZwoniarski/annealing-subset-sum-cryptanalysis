"""Generate report-ready plots from benchmark CSV files."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd

SOURCE_LABELS = {
    "random": "Random subset-sum",
    "merkle_hellman": "Merkle-Hellman",
}

SOLVER_LABELS = {
    "brute_force": "Brute force",
    "simulated_annealing": "Simulated annealing",
    "simulated_quantum_annealing": "Simulated quantum annealing",
    "exact_qubo": "Exact QUBO",
}

SOLVER_STYLES = {
    "brute_force": {"color": "#2f5f8f", "marker": "o"},
    "simulated_annealing": {"color": "#c95f27", "marker": "s"},
    "simulated_quantum_annealing": {"color": "#438a5e", "marker": "^"},
    "exact_qubo": {"color": "#6f5aa7", "marker": "D"},
}


def generate_benchmark_plots(input_csv: Path, output_dir: Path) -> list[Path]:
    data = _prepare_data(input_csv)
    output_dir.mkdir(parents=True, exist_ok=True)

    outputs = [
        _rate_plot(
            data,
            metric="exact_hit",
            output_path=output_dir / "success_rate_vs_n.png",
            y_label="Exact-hit rate",
            title="Exact subset-sum recovery",
        ),
        _metric_plot(
            data,
            metric="runtime_ms",
            aggregation="median",
            output_path=output_dir / "runtime_ms_vs_n.png",
            y_label="Median runtime [ms]",
            title="Runtime by instance size",
            yscale="log",
        ),
        _metric_plot(
            data.assign(objective_log10=np.log10(data["objective_value"] + 1)),
            metric="objective_log10",
            aggregation="median",
            output_path=output_dir / "objective_value_vs_n.png",
            y_label="Median log10(best objective + 1)",
            title="Residual objective gap",
        ),
        _metric_plot(
            data,
            metric="hamming_distance",
            aggregation="mean",
            output_path=output_dir / "hamming_distance_vs_n.png",
            y_label="Mean distance to planted bits",
            title="Recovered bit-vector distance",
        ),
    ]
    return outputs


def _prepare_data(input_csv: Path) -> pd.DataFrame:
    data = pd.read_csv(input_csv)
    if data.empty:
        raise ValueError("benchmark CSV is empty")
    data["exact_hit"] = data["exact_hit"].map(_to_bool)
    if "success" in data:
        data["success"] = data["success"].map(_to_bool)
    if "known_solution_match" in data:
        data["known_solution_match"] = data["known_solution_match"].map(_to_nullable_bool)
    return data


def _rate_plot(
    data: pd.DataFrame,
    *,
    metric: str,
    output_path: Path,
    y_label: str,
    title: str,
) -> Path:
    return _metric_plot(
        data=data,
        metric=metric,
        aggregation="mean",
        output_path=output_path,
        y_label=y_label,
        title=title,
        y_limits=(-0.04, 1.04),
        y_formatter=lambda value: f"{value:.0%}",
    )


def _metric_plot(
    data: pd.DataFrame,
    *,
    metric: str,
    aggregation: str,
    output_path: Path,
    y_label: str,
    title: str,
    yscale: str = "linear",
    y_limits: tuple[float, float] | None = None,
    y_formatter: Callable[[float], str] | None = None,
) -> Path:
    grouped = (
        data.groupby(["source", "solver", "n_bits"], as_index=False)[metric]
        .agg(aggregation)
        .sort_values(["source", "solver", "n_bits"])
    )

    sources = list(grouped["source"].drop_duplicates())
    fig, axes = plt.subplots(
        1,
        len(sources),
        figsize=(11.0, 4.8),
        sharey=True,
        constrained_layout=False,
    )
    if len(sources) == 1:
        axes = [axes]

    handles = {}
    for ax, source in zip(axes, sources):
        source_data = grouped[grouped["source"] == source]
        for solver, series in source_data.groupby("solver"):
            style = SOLVER_STYLES.get(solver, {"marker": "o"})
            (line,) = ax.plot(
                series["n_bits"],
                series[metric],
                linewidth=2.0,
                markersize=6,
                label=SOLVER_LABELS.get(solver, solver),
                **style,
            )
            handles[solver] = line

        ax.set_title(SOURCE_LABELS.get(source, source), fontsize=11)
        ax.set_xlabel("n bits")
        ax.set_xticks(sorted(data["n_bits"].unique()))
        ax.grid(True, which="major", axis="both", alpha=0.25)
        ax.set_yscale(yscale)
        if y_limits is not None:
            ax.set_ylim(*y_limits)
        if y_formatter is not None:
            ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: y_formatter(value)))

    axes[0].set_ylabel(y_label)
    fig.suptitle(title, fontsize=13, fontweight="bold")
    fig.subplots_adjust(bottom=0.24, top=0.82, wspace=0.14)
    ordered_solvers = [solver for solver in SOLVER_LABELS if solver in handles]
    fig.legend(
        [handles[solver] for solver in ordered_solvers],
        [SOLVER_LABELS[solver] for solver in ordered_solvers],
        loc="lower center",
        ncol=min(3, len(handles)),
        frameon=False,
        bbox_to_anchor=(0.5, 0.03),
    )

    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    return output_path


def _to_bool(value: object) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def _to_nullable_bool(value: object) -> bool | None:
    if pd.isna(value) or str(value).strip() == "":
        return None
    return _to_bool(value)
