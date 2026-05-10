from annealing_crypto.experiments.export_results import (
    BENCHMARK_COLUMNS,
    read_benchmark_csv,
    write_benchmark_csv,
)
from annealing_crypto.experiments.run_benchmark import BenchmarkConfig, run_benchmark
from annealing_crypto.experiments.run_benchmark import benchmark_config_from_mapping


def test_benchmark_runner_returns_one_row_per_solver_and_scenario() -> None:
    config = BenchmarkConfig(
        sizes=(4,),
        trials=1,
        sources=("random", "merkle_hellman"),
        solvers=(
            "brute_force",
            "simulated_annealing",
            "simulated_quantum_annealing",
        ),
        annealing_reads=20,
        annealing_sweeps=50,
        quantum_reads=5,
        quantum_sweeps=10,
        quantum_trotter_slices=3,
    )

    rows = run_benchmark(config)

    assert len(rows) == 6
    assert {row["source"] for row in rows} == {"random", "merkle_hellman"}
    assert {row["solver"] for row in rows} == {
        "brute_force",
        "simulated_annealing",
        "simulated_quantum_annealing",
    }
    assert all(set(BENCHMARK_COLUMNS).issubset(row) for row in rows)
    assert all(row["success"] == row["exact_hit"] for row in rows)


def test_benchmark_csv_roundtrip(tmp_path) -> None:
    output_path = tmp_path / "benchmark.csv"
    rows = run_benchmark(
        BenchmarkConfig(
            sizes=(4,),
            trials=1,
            sources=("random",),
            solvers=("brute_force",),
        )
    )

    write_benchmark_csv(rows, output_path)

    loaded = read_benchmark_csv(output_path)
    assert len(loaded) == 1
    assert loaded[0]["solver"] == "brute_force"
    assert loaded[0]["source"] == "random"


def test_benchmark_config_from_mapping_applies_overrides() -> None:
    config = benchmark_config_from_mapping(
        {
            "sizes": [8, 12],
            "trials": 3,
            "solvers": ["brute_force", "simulated_quantum_annealing"],
            "quantum_reads": 7,
            "quantum_trotter_slices": 5,
            "random_weight_max": 999,
        }
    )

    assert config.sizes == (8, 12)
    assert config.trials == 3
    assert config.solvers == ("brute_force", "simulated_quantum_annealing")
    assert config.quantum_reads == 7
    assert config.quantum_trotter_slices == 5
    assert config.random_weight_max == 999
