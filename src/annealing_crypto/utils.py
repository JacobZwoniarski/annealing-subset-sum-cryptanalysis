"""Small validation helpers shared by cryptographic toy models."""

from collections.abc import Iterable, Sequence


def normalize_bits(bits: Iterable[int]) -> tuple[int, ...]:
    """Return bits as an immutable tuple after strict binary validation."""
    normalized = tuple(int(bit) for bit in bits)
    invalid = [bit for bit in normalized if bit not in (0, 1)]
    if invalid:
        raise ValueError(f"bits must contain only 0 or 1 values, got {invalid!r}")
    return normalized


def require_same_length(left: Sequence[object], right: Sequence[object], label: str) -> None:
    if len(left) != len(right):
        raise ValueError(f"{label} length mismatch: {len(left)} != {len(right)}")
