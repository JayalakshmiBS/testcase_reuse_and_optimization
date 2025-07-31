import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic

@pytest.mark.parametrize("expression, expected", [
    ("0002+3", "5"),
    ("2 + 3", "5"),
])
def test_leading_and_whitespace_cases(expression, expected):
    calc = CalculatorLogic()
    calc.insert(expression)
    assert calc.calculate() == expected


def test_insert_leading_zero_after_operator():
    calc = CalculatorLogic()
    calc.insert('3+0')
    calc.insert('5')  # Should replace '0' after operator
    assert calc.expression == '3+5'


def test_chaining_results():
    calc = CalculatorLogic()
    calc.insert('10+5')
    calc.calculate()
    calc.insert('15*2')
    result = calc.calculate()
    assert result == '30'


def test_delete_last_empty_expression():
    calc = CalculatorLogic()
    calc.delete_last()
    assert calc.expression == ''


def test_delete_last_after_single_digit():
    calc = CalculatorLogic()
    calc.insert('7')
    calc.delete_last()
    assert calc.expression == ''


def test_valid_then_invalid_chain():
    calc = CalculatorLogic()
    calc.insert('2+2')
    calc.calculate()
    calc.insert('+')
    calc.insert('a')  # Invalid input
    result = calc.calculate()
    assert result == 'Error'


def test_multiple_valid_expressions_sequentially():
    calc = CalculatorLogic()
    calc.insert('1+1')
    result1 = calc.calculate()
    assert result1 == '2'
    
    calc.insert('2*3')
    result2 = calc.calculate()
    assert result2 == '6'
