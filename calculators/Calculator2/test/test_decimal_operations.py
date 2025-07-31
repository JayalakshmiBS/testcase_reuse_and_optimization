import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic


@pytest.fixture
def calculator():
    return CalculatorLogic()


def test_float_addition(calculator):
    calculator.insert('2.5+3.5')
    result = calculator.calculate()
    assert result == '6.0'


def test_decimal_operations(calculator):
    calculator.insert('2.5+3.5')
    result = calculator.calculate()
    assert result == '6.0'


def test_float_division(calculator):
    calculator.insert('5.0/2.0')
    result = calculator.calculate()
    assert result == '2.5'


def test_insert_number_after_decimal_point(calculator):
    calculator.insert('.')
    calculator.insert('5')
    assert calculator.expression == '.5'


def test_multiple_decimal_points_in_number(calculator):
    calculator.insert('3.14.15')
    result = calculator.calculate()
    assert result == 'Error'
