import pytest

from annealing_crypto.merkle_hellman import encrypt_bits, generate_keypair
from annealing_crypto.subset_sum import (
    SubsetSumInstance,
    instance_from_merkle_hellman,
    is_solution,
    objective_value,
    random_subset_sum_instance,
    residual,
    subset_sum_value,
)


def test_subset_sum_value_uses_selected_weights() -> None:
    assert subset_sum_value((4, 9, 15, 20), (1, 0, 1, 0)) == 19


def test_instance_validates_known_solution_against_target() -> None:
    with pytest.raises(ValueError, match="does not match"):
        SubsetSumInstance(weights=(3, 5, 8), target=9, known_solution=(1, 1, 0))


def test_solution_checks_and_objective_value() -> None:
    instance = SubsetSumInstance(
        weights=(3, 6, 10),
        target=13,
        known_solution=(1, 0, 1),
    )

    assert is_solution(instance, (1, 0, 1))
    assert residual(instance, (0, 1, 1)) == 3
    assert objective_value(instance, (0, 1, 1)) == 9


def test_random_instance_is_reproducible_and_has_known_solution() -> None:
    first = random_subset_sum_instance(8, seed=7)
    second = random_subset_sum_instance(8, seed=7)

    assert first == second
    assert first.source == "random"
    assert first.known_solution is not None
    assert is_solution(first, first.known_solution)


def test_merkle_hellman_ciphertext_becomes_subset_sum_instance() -> None:
    keypair = generate_keypair(6, seed=99)
    message = (1, 0, 0, 1, 1, 0)
    ciphertext = encrypt_bits(keypair.public, message)

    instance = instance_from_merkle_hellman(
        keypair.public,
        ciphertext,
        known_message=message,
    )

    assert instance.source == "merkle_hellman"
    assert instance.weights == keypair.public.weights
    assert instance.target == ciphertext
    assert is_solution(instance, message)


def test_subset_sum_rejects_invalid_binary_vector() -> None:
    with pytest.raises(ValueError, match="only 0 or 1"):
        subset_sum_value((1, 2, 3), (1, 0, 4))
