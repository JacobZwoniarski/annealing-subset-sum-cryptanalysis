"""CLI entry point for benchmark validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from annealing_crypto.experiments.run_benchmark import benchmark_config_from_mapping
from annealing_crypto.experiments.validate_results import validate_benchmark_csv


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("experiments/raw/benchmark.csv"),
    )
    parser.add_argument("--config", type=Path)
    args = parser.parse_args()

    config = None
    if args.config is not None:
        config = benchmark_config_from_mapping(json.loads(args.config.read_text()))

    report = validate_benchmark_csv(args.input, config=config)
    print(json.dumps(report.as_dict(), indent=2))


if __name__ == "__main__":
    main()
