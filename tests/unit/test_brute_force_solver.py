import pytest

from annealing_crypto.metrics import hamming_distance
from annealing_crypto.solvers.brute_force import solve_brute_force
from annealing_crypto.subset_sum import SubsetSumInstance, random_subset_sum_instance


def test_brute_force_finds_known_solution_for_small_instance() -> None:
    instance = SubsetSumInstance(
        weights=(4, 7, 13, 29),
        target=24,
        known_solution=(1, 1, 1, 0),
    )

    result = solve_brute_force(instance)

    assert result.exact_hit
    assert result.objective_value == 0
    assert hamming_distance(result.solution, instance.known_solution) == 0
    assert result.metadata["evaluated_states"] <= 2**instance.n_bits


def test_brute_force_can_scan_full_space_when_requested() -> None:
    instance = SubsetSumInstance(weights=(2, 4, 6), target=6)

    result = solve_brute_force(instance, stop_at_first_exact=False)

    assert result.exact_hit
    assert result.solution in ((0, 0, 1), (1, 1, 0))
    assert result.metadata["evaluated_states"] == 8


def test_brute_force_uses_objective_for_best_near_miss() -> None:
    instance = SubsetSumInstance(weights=(5, 11), target=4)

    result = solve_brute_force(instance, stop_at_first_exact=False)

    assert not result.exact_hit
    assert result.solution == (1, 0)
    assert result.objective_value == 1


def test_brute_force_refuses_large_instances_by_default() -> None:
    instance = random_subset_sum_instance(25, seed=1)

    with pytest.raises(ValueError, match="refused"):
        solve_brute_force(instance)


def test_hamming_distance_validates_lengths() -> None:
    with pytest.raises(ValueError, match="length mismatch"):
        hamming_distance((1, 0), (1, 0, 1))
