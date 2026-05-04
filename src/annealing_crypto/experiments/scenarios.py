"""Deterministic benchmark scenarios for subset-sum experiments."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Literal

from annealing_crypto.merkle_hellman import encrypt_bits, generate_keypair
from annealing_crypto.subset_sum import (
    SubsetSumInstance,
    instance_from_merkle_hellman,
    random_subset_sum_instance,
)

ScenarioSource = Literal["random", "merkle_hellman"]


@dataclass(frozen=True)
class BenchmarkScenario:
    source: ScenarioSource
    n_bits: int
    trial: int
    seed: int
    weight_min: int = 1
    weight_max: int = 100

    @property
    def scenario_id(self) -> str:
        return f"{self.source}-n{self.n_bits}-t{self.trial}-s{self.seed}"


def build_instance(scenario: BenchmarkScenario) -> SubsetSumInstance:
    if scenario.source == "random":
        return random_subset_sum_instance(
            scenario.n_bits,
            seed=scenario.seed,
            weight_min=scenario.weight_min,
            weight_max=scenario.weight_max,
        )
    if scenario.source == "merkle_hellman":
        keypair = generate_keypair(scenario.n_bits, seed=scenario.seed)
        rng = Random(scenario.seed ^ 0xA5A5)
        message = tuple(rng.randint(0, 1) for _ in range(scenario.n_bits))
        ciphertext = encrypt_bits(keypair.public, message)
        return instance_from_merkle_hellman(
            keypair.public,
            ciphertext,
            known_message=message,
        )
    raise ValueError(f"unsupported scenario source: {scenario.source}")


def iter_scenarios(
    *,
    sizes: tuple[int, ...],
    trials: int,
    base_seed: int,
    sources: tuple[ScenarioSource, ...] = ("random", "merkle_hellman"),
) -> list[BenchmarkScenario]:
    if not sizes:
        raise ValueError("sizes must not be empty")
    if trials <= 0:
        raise ValueError("trials must be positive")

    scenarios: list[BenchmarkScenario] = []
    for source_index, source in enumerate(sources):
        for n_bits in sizes:
            for trial in range(trials):
                seed = base_seed + source_index * 100_000 + n_bits * 1_000 + trial
                scenarios.append(
                    BenchmarkScenario(
                        source=source,
                        n_bits=n_bits,
                        trial=trial,
                        seed=seed,
                    )
                )
    return scenarios
