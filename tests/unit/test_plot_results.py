from annealing_crypto.experiments.export_results import write_benchmark_csv
from annealing_crypto.experiments.plot_results import generate_benchmark_plots


def test_generate_benchmark_plots_creates_expected_png_files(tmp_path) -> None:
    input_csv = tmp_path / "benchmark.csv"
    output_dir = tmp_path / "plots"
    rows = [
        {
            "scenario_id": "random-n4-t0-s1",
            "source": "random",
            "n_bits": 4,
            "trial": 0,
            "seed": 1,
            "solver": "brute_force",
            "success": True,
            "exact_hit": True,
            "objective_value": 0,
            "runtime_ms": 0.1,
            "hamming_distance": 0,
            "target": 9,
            "weight_sum": 30,
            "evaluated_states": 8,
        },
        {
            "scenario_id": "random-n4-t0-s1",
            "source": "random",
            "n_bits": 4,
            "trial": 0,
            "seed": 1,
            "solver": "simulated_annealing",
            "success": True,
            "exact_hit": True,
            "objective_value": 0,
            "runtime_ms": 1.2,
            "hamming_distance": 0,
            "target": 9,
            "weight_sum": 30,
            "num_reads": 20,
            "num_sweeps": 50,
        },
    ]
    write_benchmark_csv(rows, input_csv)

    outputs = generate_benchmark_plots(input_csv, output_dir)

    assert [path.name for path in outputs] == [
        "success_rate_vs_n.png",
        "runtime_ms_vs_n.png",
        "objective_value_vs_n.png",
    ]
    assert all(path.exists() and path.stat().st_size > 0 for path in outputs)
