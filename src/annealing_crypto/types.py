"""Shared result structures returned by solvers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SolverResult:
    solver: str
    solution: tuple[int, ...]
    objective_value: int | float
    runtime_ms: float
    exact_hit: bool
    metadata: dict[str, Any] = field(default_factory=dict)
