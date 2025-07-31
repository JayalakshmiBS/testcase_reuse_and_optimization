import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import modulus


@pytest.mark.parametrize("x, y, expected", [
    (10, 3, 1),
    (15, 4, 3)
])
def test_modulus_positive_numbers(x, y, expected):
    assert modulus(x, y) == expected


@pytest.mark.parametrize("x, y, expected", [
    (-10, 3, -10 % 3),
    (10, -3, 10 % -3),
    (-10, -3, -10 % -3)
])
def test_modulus_negative_numbers(x, y, expected):
    assert modulus(x, y) == expected


@pytest.mark.parametrize("x, y, expected", [
    (5.5, 2.0, 1.5),
    (10.0, 3.0, 1.0)
])
def test_modulus_floats(x, y, expected):
    assert pytest.approx(modulus(x, y), rel=1e-6) == expected


def test_modulus_by_zero():
    assert modulus(10, 0) == "Cannot perform modulus by zero"
