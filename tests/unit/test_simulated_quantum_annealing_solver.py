import pytest

from annealing_crypto.metrics import hamming_distance
from annealing_crypto.solvers.simulated_quantum_annealing import (
    solve_simulated_quantum_annealing,
)
from annealing_crypto.subset_sum import SubsetSumInstance


def test_simulated_quantum_annealing_solves_tiny_instance() -> None:
    instance = SubsetSumInstance(
        weights=(2, 5, 11),
        target=7,
        known_solution=(1, 1, 0),
    )

    result = solve_simulated_quantum_annealing(
        instance,
        num_reads=20,
        num_sweeps=80,
        trotter_slices=4,
        beta=0.05,
        seed=123,
    )

    assert result.exact_hit
    assert result.objective_value == 0
    assert hamming_distance(result.solution, instance.known_solution) == 0


def test_simulated_quantum_annealing_reports_parameters() -> None:
    instance = SubsetSumInstance(weights=(2, 5), target=7, known_solution=(1, 1))

    result = solve_simulated_quantum_annealing(
        instance,
        num_reads=3,
        num_sweeps=5,
        trotter_slices=3,
        beta=0.1,
        seed=7,
    )

    assert result.metadata["num_reads"] == 3
    assert result.metadata["num_sweeps"] == 5
    assert result.metadata["trotter_slices"] == 3
    assert result.metadata["beta"] == 0.1
    assert result.metadata["seed"] == 7


@pytest.mark.parametrize(
    "kwargs",
    [
        {"num_reads": 0},
        {"num_sweeps": 0},
        {"trotter_slices": 1},
        {"beta": 0},
        {"transverse_field_start": 0},
        {"transverse_field_end": 3.0},
    ],
)
def test_simulated_quantum_annealing_validates_parameters(kwargs) -> None:
    instance = SubsetSumInstance(weights=(2, 5), target=7)

    with pytest.raises(ValueError):
        solve_simulated_quantum_annealing(instance, **kwargs)
