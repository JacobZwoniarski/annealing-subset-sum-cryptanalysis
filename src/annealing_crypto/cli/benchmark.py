"""CLI entry point for benchmark CSV generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from annealing_crypto.experiments.export_results import write_benchmark_csv
from annealing_crypto.experiments.run_benchmark import BenchmarkConfig, run_benchmark


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/raw/benchmark.csv"),
    )
    parser.add_argument("--sizes", type=int, nargs="+", default=[8, 12, 16])
    parser.add_argument("--trials", type=int, default=5)
    parser.add_argument("--annealing-reads", type=int, default=100)
    parser.add_argument("--annealing-sweeps", type=int, default=1_000)
    args = parser.parse_args()

    config = BenchmarkConfig(
        sizes=tuple(args.sizes),
        trials=args.trials,
        annealing_reads=args.annealing_reads,
        annealing_sweeps=args.annealing_sweeps,
    )
    rows = run_benchmark(config)
    write_benchmark_csv(rows, args.output)
    print(f"wrote {len(rows)} rows to {args.output}")


if __name__ == "__main__":
    main()
