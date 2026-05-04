"""Small Merkle-Hellman demo for a fixed toy instance."""

from annealing_crypto.merkle_hellman import (
    decrypt_ciphertext,
    encrypt_bits,
    generate_keypair,
)


def main() -> None:
    keypair = generate_keypair(8, seed=42)
    message = (1, 0, 1, 1, 0, 0, 1, 0)
    ciphertext = encrypt_bits(keypair.public, message)
    recovered = decrypt_ciphertext(keypair.private, ciphertext)

    print(f"public_weights={keypair.public.weights}")
    print(f"message={message}")
    print(f"ciphertext={ciphertext}")
    print(f"recovered={recovered}")


if __name__ == "__main__":
    main()
