import pytest

from annealing_crypto.qubo import (
    build_subset_sum_bqm,
    build_subset_sum_qubo,
    sample_to_bits,
)
from annealing_crypto.solvers.exact_qubo import solve_exact_qubo
from annealing_crypto.subset_sum import SubsetSumInstance, objective_value


def test_qubo_energy_matches_subset_sum_objective() -> None:
    instance = SubsetSumInstance(
        weights=(3, 6, 10),
        target=13,
        known_solution=(1, 0, 1),
    )
    bqm = build_subset_sum_bqm(instance)

    for bits in ((0, 0, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)):
        sample = dict(enumerate(bits))
        assert bqm.energy(sample) == objective_value(instance, bits)


def test_qubo_contains_expected_linear_and_quadratic_terms() -> None:
    instance = SubsetSumInstance(weights=(2, 5), target=7)

    qubo, offset = build_subset_sum_qubo(instance)

    assert qubo[(0, 0)] == -24.0
    assert qubo[(1, 1)] == -45.0
    assert qubo[(0, 1)] == 20.0
    assert offset == 49.0


def test_exact_qubo_solver_finds_small_subset_solution() -> None:
    instance = SubsetSumInstance(
        weights=(4, 7, 13, 29),
        target=24,
        known_solution=(1, 1, 1, 0),
    )

    result = solve_exact_qubo(instance)

    assert result.exact_hit
    assert result.solution == instance.known_solution
    assert result.objective_value == 0


def test_exact_qubo_refuses_large_instances_by_default() -> None:
    instance = SubsetSumInstance(weights=tuple(range(1, 22)), target=10)

    with pytest.raises(ValueError, match="refused"):
        solve_exact_qubo(instance)


def test_sample_to_bits_orders_variables_by_index() -> None:
    assert sample_to_bits({2: 1, 0: 0, 1: 1}, 3) == (0, 1, 1)
