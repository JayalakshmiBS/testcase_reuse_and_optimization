import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import multiply

@pytest.mark.parametrize("values, expected", [
    ([2, 3, 4], 24),
    ([5, 10], 50)
])
def test_multiply_positive_numbers(values, expected):
    assert multiply(values) == expected


@pytest.mark.parametrize("values, expected", [
    ([10, 0, 5], 0),
    ([0, -3], 0),
    ([0, -3], 0)  # Repeated to match the separate original test
])
def test_multiply_with_zero_and_negative(values, expected):
    assert multiply(values) == expected


@pytest.mark.parametrize("values, expected", [
    ([-1, 2], -2),
    ([-2, -3], 6)
])
def test_multiply_negative_numbers(values, expected):
    assert multiply(values) == expected


@pytest.mark.parametrize("values, expected", [
    ([1.5, 2.0], 3.0),
    ([0.1, 0.1], 0.01)
])
def test_multiply_floats(values, expected):
    assert pytest.approx(multiply(values), rel=1e-6) == expected


def test_multiply_empty_list():
    assert multiply([]) == 1


@pytest.mark.parametrize("values, expected", [
    ([5], 5),
    ([-3], -3)
])
def test_multiply_single_element(values, expected):
    assert multiply(values) == expected
