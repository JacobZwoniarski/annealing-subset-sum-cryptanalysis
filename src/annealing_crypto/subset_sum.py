"""Subset-sum instances used by baseline and QUBO solvers."""

from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Iterable

from annealing_crypto.merkle_hellman import MerkleHellmanPublicKey
from annealing_crypto.utils import normalize_bits, require_same_length


@dataclass(frozen=True)
class SubsetSumInstance:
    weights: tuple[int, ...]
    target: int
    known_solution: tuple[int, ...] | None = None
    source: str = "unknown"

    def __post_init__(self) -> None:
        if not self.weights:
            raise ValueError("subset-sum instance must contain at least one weight")
        if any(weight <= 0 for weight in self.weights):
            raise ValueError("subset-sum weights must be positive")
        if self.target < 0:
            raise ValueError("subset-sum target must be non-negative")
        if self.known_solution is not None:
            solution = normalize_bits(self.known_solution)
            require_same_length(self.weights, solution, "weights/known solution")
            if subset_sum_value(self.weights, solution) != self.target:
                raise ValueError("known solution does not match the target")
            object.__setattr__(self, "known_solution", solution)

    @property
    def n_bits(self) -> int:
        return len(self.weights)


def subset_sum_value(weights: Iterable[int], bits: Iterable[int]) -> int:
    weights_tuple = tuple(weights)
    bits_tuple = normalize_bits(bits)
    require_same_length(weights_tuple, bits_tuple, "weights/bits")
    return sum(weight for weight, bit in zip(weights_tuple, bits_tuple) if bit)


def residual(instance: SubsetSumInstance, bits: Iterable[int]) -> int:
    return subset_sum_value(instance.weights, bits) - instance.target


def objective_value(instance: SubsetSumInstance, bits: Iterable[int]) -> int:
    gap = residual(instance, bits)
    return gap * gap


def is_solution(instance: SubsetSumInstance, bits: Iterable[int]) -> bool:
    return residual(instance, bits) == 0


def random_subset_sum_instance(
    n_bits: int,
    *,
    seed: int | None = None,
    weight_min: int = 1,
    weight_max: int = 100,
) -> SubsetSumInstance:
    if n_bits <= 0:
        raise ValueError("n_bits must be positive")
    if weight_min <= 0:
        raise ValueError("weight_min must be positive")
    if weight_max < weight_min:
        raise ValueError("weight_max must be greater than or equal to weight_min")

    rng = Random(seed)
    weights = tuple(rng.randint(weight_min, weight_max) for _ in range(n_bits))
    solution = tuple(rng.randint(0, 1) for _ in range(n_bits))
    target = subset_sum_value(weights, solution)
    return SubsetSumInstance(
        weights=weights,
        target=target,
        known_solution=solution,
        source="random",
    )


def instance_from_merkle_hellman(
    public_key: MerkleHellmanPublicKey,
    ciphertext: int,
    *,
    known_message: Iterable[int] | None = None,
) -> SubsetSumInstance:
    solution = None if known_message is None else normalize_bits(known_message)
    return SubsetSumInstance(
        weights=public_key.weights,
        target=ciphertext,
        known_solution=solution,
        source="merkle_hellman",
    )
