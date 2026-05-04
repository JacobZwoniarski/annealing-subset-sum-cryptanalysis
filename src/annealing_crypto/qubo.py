"""QUBO encoding for the subset-sum objective."""

from __future__ import annotations

import dimod

from annealing_crypto.subset_sum import SubsetSumInstance

Qubo = dict[tuple[int, int], float]


def build_subset_sum_qubo(instance: SubsetSumInstance) -> tuple[Qubo, float]:
    """Encode E(x) = (sum(a_i x_i) - target)^2 as a QUBO matrix."""
    qubo: Qubo = {}
    weights = instance.weights

    for i, weight in enumerate(weights):
        qubo[(i, i)] = float(weight * weight - 2 * instance.target * weight)

    for i, left in enumerate(weights):
        for j in range(i + 1, len(weights)):
            qubo[(i, j)] = float(2 * left * weights[j])

    offset = float(instance.target * instance.target)
    return qubo, offset


def build_subset_sum_bqm(instance: SubsetSumInstance) -> dimod.BinaryQuadraticModel:
    qubo, offset = build_subset_sum_qubo(instance)
    return dimod.BinaryQuadraticModel.from_qubo(qubo, offset=offset)


def sample_to_bits(sample: dict[int, int], n_bits: int) -> tuple[int, ...]:
    return tuple(int(sample[index]) for index in range(n_bits))
