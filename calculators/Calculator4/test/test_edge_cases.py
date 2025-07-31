import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import subtract, calculate


def test_subtract_empty():
    assert subtract([]) == 0


def test_calculate_add_missing_values():
    with pytest.raises(TypeError):
        calculate('1')


def test_calculate_subtract_missing_values():
    result = calculate('2')
    assert result is None or result == 0


def test_calculate_subtract_with_values():
    assert calculate('2', values=[10, 2]) == 8


@pytest.mark.parametrize("operation", ['3'])
def test_calculate_multiply_missing_values(operation):
    with pytest.raises(TypeError):
        calculate(operation)


@pytest.mark.parametrize("kwargs", [{'y': 2}, {'x': 2}])
def test_calculate_divide_missing_xy(kwargs):
    with pytest.raises(TypeError):
        calculate('4', **kwargs)


def test_calculate_add_values_none():
    with pytest.raises(TypeError):
        calculate('1', values=None)
