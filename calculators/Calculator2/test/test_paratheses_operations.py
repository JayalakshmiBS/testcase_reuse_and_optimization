import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic

@pytest.mark.parametrize("expression, expected", [
    ("-(2+3)", "-5"),
    ("((2+3)*(4+5))", "45"),
    ("((1+2)*3+4)/2", "6.5"),
])
def test_valid_parentheses_expressions(expression, expected):
    calc = CalculatorLogic()
    calc.insert(expression)
    assert calc.calculate() == expected


def test_expression_with_leading_zeros():
    calc = CalculatorLogic()
    for char in "002+03":
        calc.insert(char)
    assert calc.calculate() == "5"


def test_cancel_then_input():
    calc = CalculatorLogic()
    calc.expression = "123"
    calc.cancel()
    calc.insert("4")
    assert calc.expression == "4"


def test_multiple_cancels():
    calc = CalculatorLogic()
    calc.expression = "123"
    calc.cancel()
    calc.cancel()  # Should remain empty
    assert calc.expression == ""
