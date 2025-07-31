import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import subtract

@pytest.mark.parametrize("values, expected", [
    ([10, 2, 3], 5),
    ([100, 50], 50)
])
def test_subtract_positive_numbers(values, expected):
    assert subtract(values) == expected


@pytest.mark.parametrize("values, expected", [
    ([-10, -5], -5),
    ([-20, -10, -5], -5)
])
def test_subtract_negative_numbers(values, expected):
    assert subtract(values) == expected


@pytest.mark.parametrize("values, expected", [
    ([42], 42),
    ([0.0], 0.0)
])
def test_subtract_single_element(values, expected):
    assert subtract(values) == expected


def test_subtract_empty_list_returns_zero():
    assert subtract([]) == 0


@pytest.mark.parametrize("values, expected", [
    ([5.5, 2.2], 3.3),
    ([1e10, 1e10], 0.0)
])
def test_subtract_floats(values, expected):
    assert pytest.approx(subtract(values), rel=1e-6) == expected


def test_subtract_float_zero():
    assert subtract([0.0]) == 0.0


def test_subtract_with_invalid_types():
    with pytest.raises(TypeError):
        subtract(["a", 2])
