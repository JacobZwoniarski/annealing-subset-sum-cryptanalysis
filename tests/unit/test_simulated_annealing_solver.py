import pytest

from annealing_crypto.metrics import hamming_distance
from annealing_crypto.solvers.simulated_annealing import solve_simulated_annealing
from annealing_crypto.subset_sum import SubsetSumInstance


def test_simulated_annealing_solves_tiny_instance_with_fixed_seed() -> None:
    instance = SubsetSumInstance(
        weights=(2, 5, 11),
        target=7,
        known_solution=(1, 1, 0),
    )

    result = solve_simulated_annealing(
        instance,
        num_reads=50,
        num_sweeps=200,
        seed=123,
    )

    assert result.exact_hit
    assert result.objective_value == 0
    assert hamming_distance(result.solution, instance.known_solution) == 0


def test_simulated_annealing_returns_requested_parameters_in_metadata() -> None:
    instance = SubsetSumInstance(weights=(3, 8), target=11, known_solution=(1, 1))

    result = solve_simulated_annealing(
        instance,
        num_reads=7,
        num_sweeps=30,
        seed=77,
    )

    assert result.metadata["num_reads"] == 7
    assert result.metadata["num_sweeps"] == 30
    assert result.metadata["seed"] == 77


@pytest.mark.parametrize("num_reads,num_sweeps", [(0, 10), (10, 0)])
def test_simulated_annealing_rejects_invalid_parameters(
    num_reads: int,
    num_sweeps: int,
) -> None:
    instance = SubsetSumInstance(weights=(3, 8), target=11)

    with pytest.raises(ValueError, match="must be positive"):
        solve_simulated_annealing(
            instance,
            num_reads=num_reads,
            num_sweeps=num_sweeps,
        )
