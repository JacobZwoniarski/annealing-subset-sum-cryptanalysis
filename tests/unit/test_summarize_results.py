import pytest

from annealing_crypto.experiments.export_results import write_benchmark_csv
from annealing_crypto.experiments.summarize_results import (
    SUMMARY_COLUMNS,
    summarize_benchmark,
    write_summary_csv,
)


def test_summarize_benchmark_groups_solver_results(tmp_path) -> None:
    input_csv = tmp_path / "benchmark.csv"
    rows = [
        _row("random-n4-t0-s1", "random", 4, "brute_force", True, 0.2, 0, 0),
        _row("random-n4-t1-s2", "random", 4, "brute_force", False, 0.4, 9, 2),
        _row("random-n4-t0-s1", "random", 4, "simulated_annealing", True, 1.2, 0, 0),
        _row(
            "random-n4-t0-s1",
            "random",
            4,
            "simulated_quantum_annealing",
            False,
            1.8,
            4,
            1,
        ),
    ]
    write_benchmark_csv(rows, input_csv)

    summary = summarize_benchmark(input_csv)

    assert list(summary.columns) == list(SUMMARY_COLUMNS)
    brute_force = summary[summary["solver"] == "brute_force"].iloc[0]
    assert brute_force["trials"] == 2
    assert brute_force["success_rate"] == 0.5
    assert brute_force["mean_runtime_ms"] == pytest.approx(0.3)
    assert brute_force["median_objective_value"] == pytest.approx(4.5)
    assert brute_force["mean_hamming_distance"] == pytest.approx(1.0)


def test_write_summary_csv_creates_processed_file(tmp_path) -> None:
    input_csv = tmp_path / "benchmark.csv"
    output_csv = tmp_path / "processed" / "summary.csv"
    write_benchmark_csv(
        [_row("mh-n4-t0-s1", "merkle_hellman", 4, "brute_force", True, 0.1, 0, 0)],
        input_csv,
    )

    write_summary_csv(input_csv, output_csv)

    assert output_csv.exists()
    assert "success_rate" in output_csv.read_text(encoding="utf-8")


def _row(
    scenario_id: str,
    source: str,
    n_bits: int,
    solver: str,
    success: bool,
    runtime_ms: float,
    objective_value: int,
    hamming_distance: int,
) -> dict[str, object]:
    return {
        "scenario_id": scenario_id,
        "source": source,
        "n_bits": n_bits,
        "trial": 0,
        "seed": 1,
        "solver": solver,
        "success": success,
        "exact_hit": objective_value == 0,
        "objective_value": objective_value,
        "runtime_ms": runtime_ms,
        "hamming_distance": hamming_distance,
        "target": 10,
        "weight_sum": 40,
    }
