import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic

@pytest.fixture
def calc():
    return CalculatorLogic()

@pytest.mark.parametrize("expression, expected", [
    ("", "Error"),
    ("5@2", "Error"),
    ("5/0", "Error"),
    ("3+", "Error"),
    ("(5+2", "Error"),
    ("foo(5)", "Error")
])
def test_invalid_and_error_cases(calc, expression, expected):
    calc.insert(expression)
    assert calc.calculate() == expected


def test_float_leading_decimal(calc):
    calc.insert('.5 + .5')
    assert calc.calculate() == '1.0'


def test_nested_parentheses(calc):
    calc.insert('((2+3)*2)')
    assert calc.calculate() == '10'


def test_large_number_scientific_notation(calc):
    calc.insert('1000000*1000000')
    result = calc.calculate()
    assert result.replace('.', '').isdigit() or 'e' in result.lower()


def test_multiple_operations(calc):
    calc.insert('2 + 3 * 4')
    assert calc.calculate() == '14'
