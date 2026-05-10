from math import gcd

import pytest

from annealing_crypto.merkle_hellman import (
    MerkleHellmanPublicKey,
    decrypt_ciphertext,
    encrypt_bits,
    generate_keypair,
    generate_superincreasing_sequence,
    is_superincreasing,
)


def test_superincreasing_sequence_validation() -> None:
    assert is_superincreasing((2, 3, 7, 15))
    assert not is_superincreasing((2, 3, 5, 11))


def test_generated_private_key_has_required_trapdoor_properties() -> None:
    keypair = generate_keypair(10, seed=123)
    private = keypair.private

    assert is_superincreasing(private.weights)
    assert private.modulus > sum(private.weights)
    assert gcd(private.multiplier, private.modulus) == 1
    assert keypair.public.weights == tuple(
        (private.multiplier * weight) % private.modulus
        for weight in private.weights
    )


def test_encrypt_bits_is_public_knapsack_sum() -> None:
    public_key = MerkleHellmanPublicKey(weights=(17, 9, 42, 31))

    ciphertext = encrypt_bits(public_key, (1, 0, 1, 1))

    assert ciphertext == 17 + 42 + 31


def test_decrypt_roundtrip_for_many_messages() -> None:
    messages = [
        (0, 0, 0, 0, 0, 0),
        (1, 0, 1, 0, 1, 0),
        (0, 1, 0, 1, 0, 1),
        (1, 1, 1, 1, 1, 1),
    ]
    for seed in range(20):
        keypair = generate_keypair(6, seed=seed)
        for message in messages:
            ciphertext = encrypt_bits(keypair.public, message)

            assert decrypt_ciphertext(keypair.private, ciphertext) == message


def test_decrypt_roundtrip_for_benchmark_sized_keys() -> None:
    for n_bits in (8, 12, 16):
        for seed in range(20260504, 20260509):
            keypair = generate_keypair(n_bits, seed=seed + n_bits * 1_000)
            message = tuple((seed + index) % 2 for index in range(n_bits))
            ciphertext = encrypt_bits(keypair.public, message)

            assert is_superincreasing(keypair.private.weights)
            assert decrypt_ciphertext(keypair.private, ciphertext) == message


def test_encrypt_rejects_wrong_message_length() -> None:
    public_key = MerkleHellmanPublicKey(weights=(1, 2, 3))

    with pytest.raises(ValueError, match="length mismatch"):
        encrypt_bits(public_key, (1, 0))


def test_encrypt_rejects_non_binary_values() -> None:
    public_key = MerkleHellmanPublicKey(weights=(1, 2, 3))

    with pytest.raises(ValueError, match="only 0 or 1"):
        encrypt_bits(public_key, (1, 2, 0))


def test_generated_superincreasing_sequence_requires_positive_size() -> None:
    with pytest.raises(ValueError, match="n_bits must be positive"):
        generate_superincreasing_sequence(0)
