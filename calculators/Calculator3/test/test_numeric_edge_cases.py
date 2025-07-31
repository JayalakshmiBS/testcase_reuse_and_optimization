import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_long_expression(calculator):
    expr = "1+2-3*4/2+(6-1)"
    calculator.expression = expr
    assert calculator.evaluate() == str(eval(expr))

def test_leading_zeros(calculator):
    calculator.expression = "007+03"
    assert calculator.evaluate() == "10"

def test_leading_zeros_in_middle_expression(calculator):
    calculator.expression = "2+005+1"
    assert calculator.evaluate() == "8"

def test_float_input(calculator):
    calculator.expression = "5.5+2.3"
    assert calculator.evaluate() == str(eval("5.5+2.3"))

def test_decimal_expression(calculator):
    calculator.expression = "0.1+0.2"
    assert round(float(calculator.evaluate()), 1) == 0.3

def test_complex_decimal_expression(calculator):
    calculator.expression = "1.5*4.2-2.1/3.5"
    expected = eval("1.5*4.2-2.1/3.5")
    assert round(float(calculator.evaluate()), 5) == round(expected, 5)

def test_negative_number(calculator):
    calculator.expression = "-5+3"
    assert calculator.evaluate() == "-2"

def test_power_operator(calculator):
    calculator.expression = "2**3"
    assert calculator.evaluate() == "8"
