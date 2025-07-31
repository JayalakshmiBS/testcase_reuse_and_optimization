import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic


@pytest.fixture
def calculator():
    return CalculatorLogic()


def test_empty_expression_calculate(calculator):
    result = calculator.calculate()
    assert result == 'Error'


def test_cancel_after_error(calculator):
    """Test cancel() after error state"""
    calculator.expression = "Error"
    result = calculator.cancel()
    assert result == ""
    assert not calculator.result_shown


def test_cancel_with_whitespace(calculator):
    """Test cancel() clears whitespace-only input"""
    calculator.expression = "   "
    result = calculator.cancel()
    assert result == ""


def test_leading_zero(calculator):
    calculator.insert('0002+3')
    result = calculator.calculate()
    assert result == '5'


def test_large_numbers(calculator):
    calculator.insert('1000000000+2000000000')
    result = calculator.calculate()
    assert result == '3000000000'


def test_large_number_of_digits(calculator):
    calculator.insert('99999999999+1')
    result = calculator.calculate()
    assert result == '100000000000'


def test_long_arithmetic_expression(calculator):
    calculator.insert('1+2+3+4+5+6+7+8+9+10')
    result = calculator.calculate()
    assert result == '55'


def test_chaining_results(calculator):
    calculator.insert('10+5')
    calculator.calculate()
    calculator.insert('15*2')
    result = calculator.calculate()
    assert result == '30'


def test_insert_operator_only(calculator):
    calculator.insert('+')
    assert calculator.expression == '+'


def test_insert_after_result(calculator):
    calculator.insert('4')
    calculator.insert('+')
    calculator.insert('4')
    calculator.calculate()  # result is '8'
    calculator.insert('*')
    calculator.insert('2')
    result = calculator.calculate()
    assert result == '16'
