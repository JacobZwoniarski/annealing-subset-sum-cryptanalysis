from annealing_crypto.merkle_hellman import (
    decrypt_ciphertext,
    encrypt_bits,
    generate_keypair,
)
from annealing_crypto.solvers.brute_force import solve_brute_force
from annealing_crypto.solvers.exact_qubo import solve_exact_qubo
from annealing_crypto.subset_sum import instance_from_merkle_hellman


def test_merkle_hellman_ciphertext_can_be_recovered_as_subset_sum() -> None:
    keypair = generate_keypair(6, seed=2026)
    message = (1, 0, 1, 1, 0, 1)
    ciphertext = encrypt_bits(keypair.public, message)
    instance = instance_from_merkle_hellman(
        keypair.public,
        ciphertext,
        known_message=message,
    )

    assert decrypt_ciphertext(keypair.private, ciphertext) == message
    assert solve_brute_force(instance).solution == message
    assert solve_exact_qubo(instance).solution == message
