"""Metrics used to compare recovered bit vectors."""

from typing import Iterable

from annealing_crypto.utils import normalize_bits, require_same_length


def hamming_distance(left: Iterable[int], right: Iterable[int]) -> int:
    left_bits = normalize_bits(left)
    right_bits = normalize_bits(right)
    require_same_length(left_bits, right_bits, "hamming operands")
    return sum(a != b for a, b in zip(left_bits, right_bits))
