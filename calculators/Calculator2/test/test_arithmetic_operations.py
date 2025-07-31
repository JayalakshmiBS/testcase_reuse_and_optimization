import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic


@pytest.fixture
def calculator():
    return CalculatorLogic()


def test_calculate_valid_expression(calculator):
    calculator.insert('2+3')
    result = calculator.calculate()
    assert result == '5'


def test_operator_precedence(calculator):
    calculator.insert('2+3*4')
    result = calculator.calculate()
    assert result == '14'


def test_large_numbers(calculator):
    calculator.insert('1000000000+2000000000')
    result = calculator.calculate()
    assert result == '3000000000'


def test_long_arithmetic_expression(calculator):
    calculator.insert('1+2+3+4+5+6+7+8+9+10')
    result = calculator.calculate()
    assert result == '55'


def test_large_number_of_digits(calculator):
    calculator.insert('99999999999+1')
    result = calculator.calculate()
    assert result == '100000000000'


def test_unary_minus_middle(calculator):
    calculator.insert('5*-2')
    result = calculator.calculate()
    assert result == '-10'


def test_negative_number(calculator):
    calculator.insert('-4+6')
    result = calculator.calculate()
    assert result == '2'


def test_start_with_operator(calculator):
    calculator.insert('+3')
    result = calculator.calculate()
    assert result == '3'
