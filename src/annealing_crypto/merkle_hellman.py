"""Toy Merkle-Hellman knapsack cryptosystem.

This module is intentionally small and explicit. It supports experiments on
educational instances where a public knapsack ciphertext becomes a subset-sum
attack instance.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from random import Random
from typing import Iterable

from annealing_crypto.utils import normalize_bits, require_same_length


@dataclass(frozen=True)
class MerkleHellmanPrivateKey:
    weights: tuple[int, ...]
    modulus: int
    multiplier: int


@dataclass(frozen=True)
class MerkleHellmanPublicKey:
    weights: tuple[int, ...]


@dataclass(frozen=True)
class MerkleHellmanKeyPair:
    public: MerkleHellmanPublicKey
    private: MerkleHellmanPrivateKey


def is_superincreasing(weights: Iterable[int]) -> bool:
    total = 0
    for weight in weights:
        if weight <= total:
            return False
        total += weight
    return True


def generate_superincreasing_sequence(
    n_bits: int,
    *,
    rng: Random | None = None,
    slack: int = 10,
) -> tuple[int, ...]:
    """Generate a positive superincreasing sequence."""
    if n_bits <= 0:
        raise ValueError("n_bits must be positive")
    if slack < 1:
        raise ValueError("slack must be positive")

    rng = rng or Random()
    weights: list[int] = []
    total = 0
    for _ in range(n_bits):
        lower = total + 1
        upper = lower + max(slack, total + slack)
        weight = rng.randint(lower, upper)
        weights.append(weight)
        total += weight
    return tuple(weights)


def generate_keypair(n_bits: int, *, seed: int | None = None) -> MerkleHellmanKeyPair:
    """Generate a toy Merkle-Hellman keypair for an n-bit message."""
    rng = Random(seed)
    private_weights = generate_superincreasing_sequence(n_bits, rng=rng)
    total = sum(private_weights)
    modulus = rng.randint(total + 1, 2 * total + 1)
    multiplier = _choose_coprime_multiplier(modulus, rng)
    public_weights = tuple((multiplier * weight) % modulus for weight in private_weights)

    private = MerkleHellmanPrivateKey(
        weights=private_weights,
        modulus=modulus,
        multiplier=multiplier,
    )
    return MerkleHellmanKeyPair(
        public=MerkleHellmanPublicKey(weights=public_weights),
        private=private,
    )


def encrypt_bits(public_key: MerkleHellmanPublicKey, bits: Iterable[int]) -> int:
    message = normalize_bits(bits)
    require_same_length(public_key.weights, message, "public key/message")
    return sum(weight for weight, bit in zip(public_key.weights, message) if bit)


def decrypt_ciphertext(private_key: MerkleHellmanPrivateKey, ciphertext: int) -> tuple[int, ...]:
    """Legally decrypt a ciphertext using the private superincreasing trapdoor."""
    _validate_private_key(private_key)
    inverse = pow(private_key.multiplier, -1, private_key.modulus)
    target = (ciphertext * inverse) % private_key.modulus
    return _solve_superincreasing(private_key.weights, target)


def _choose_coprime_multiplier(modulus: int, rng: Random) -> int:
    candidates = list(range(2, modulus))
    rng.shuffle(candidates)
    for candidate in candidates:
        if gcd(candidate, modulus) == 1:
            return candidate
    raise ValueError(f"could not find coprime multiplier for modulus={modulus}")


def _solve_superincreasing(weights: tuple[int, ...], target: int) -> tuple[int, ...]:
    bits = [0] * len(weights)
    remaining = target
    for index in range(len(weights) - 1, -1, -1):
        weight = weights[index]
        if weight <= remaining:
            bits[index] = 1
            remaining -= weight
    if remaining != 0:
        raise ValueError("ciphertext does not decode to a valid superincreasing subset")
    return tuple(bits)


def _validate_private_key(private_key: MerkleHellmanPrivateKey) -> None:
    if not private_key.weights:
        raise ValueError("private key must contain at least one weight")
    if not is_superincreasing(private_key.weights):
        raise ValueError("private weights must be superincreasing")
    if private_key.modulus <= sum(private_key.weights):
        raise ValueError("modulus must be greater than the private weight sum")
    if gcd(private_key.multiplier, private_key.modulus) != 1:
        raise ValueError("multiplier must be coprime with modulus")
