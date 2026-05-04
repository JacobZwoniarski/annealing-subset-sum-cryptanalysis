"""CLI entry point for plot generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from annealing_crypto.experiments.plot_results import generate_benchmark_plots


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("experiments/raw/benchmark.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/plots"),
    )
    args = parser.parse_args()

    outputs = generate_benchmark_plots(args.input, args.output_dir)
    for output in outputs:
        print(output)


if __name__ == "__main__":
    main()
