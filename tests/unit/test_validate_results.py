import pytest

from annealing_crypto.experiments.export_results import write_benchmark_csv
from annealing_crypto.experiments.run_benchmark import BenchmarkConfig, run_benchmark
from annealing_crypto.experiments.validate_results import validate_benchmark_csv


def test_validate_benchmark_csv_accepts_generated_rows(tmp_path) -> None:
    config = BenchmarkConfig(
        sizes=(4,),
        trials=1,
        sources=("random",),
        solvers=("brute_force", "simulated_annealing"),
        annealing_reads=10,
        annealing_sweeps=20,
    )
    output_path = tmp_path / "benchmark.csv"
    write_benchmark_csv(run_benchmark(config), output_path)

    report = validate_benchmark_csv(output_path, config=config)

    assert report.ok
    assert report.rows == 2
    assert "row count and benchmark grid match config" in report.checks


def test_validate_benchmark_csv_rejects_inconsistent_exact_hit(tmp_path) -> None:
    output_path = tmp_path / "benchmark.csv"
    rows = run_benchmark(
        BenchmarkConfig(
            sizes=(4,),
            trials=1,
            sources=("random",),
            solvers=("brute_force",),
        )
    )
    rows[0]["exact_hit"] = False
    write_benchmark_csv(rows, output_path)

    with pytest.raises(ValueError, match="exact_hit"):
        validate_benchmark_csv(output_path)


def test_validate_benchmark_csv_rejects_duplicate_grid_key(tmp_path) -> None:
    config = BenchmarkConfig(
        sizes=(4,),
        trials=2,
        sources=("random",),
        solvers=("brute_force",),
    )
    rows = run_benchmark(config)
    rows[1] = dict(rows[0])
    output_path = tmp_path / "benchmark.csv"
    write_benchmark_csv(rows, output_path)

    with pytest.raises(ValueError, match="duplicate benchmark rows"):
        validate_benchmark_csv(output_path, config=config)
