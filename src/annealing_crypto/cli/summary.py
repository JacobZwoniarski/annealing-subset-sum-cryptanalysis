"""CLI entry point for processed benchmark summaries."""

from __future__ import annotations

import argparse
from pathlib import Path

from annealing_crypto.experiments.summarize_results import write_summary_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("experiments/raw/benchmark.csv"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/processed/summary.csv"),
    )
    args = parser.parse_args()

    write_summary_csv(args.input, args.output)
    print(f"wrote summary to {args.output}")


if __name__ == "__main__":
    main()
