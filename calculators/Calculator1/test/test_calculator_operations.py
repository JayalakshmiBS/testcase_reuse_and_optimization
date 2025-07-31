import pytest
import sys
import os,math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calc_logic import CalculatorLogic


@pytest.fixture
def calc():
    return CalculatorLogic()

def test_parentheses(calc):
    calc.add_to_expression(3)
    calc.append_operator("*")
    calc.add_to_expression("(")
    calc.add_to_expression(4)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.add_to_expression(")")
    calc.evaluate()
    assert calc.current_expression == "18"

def test_multiple_parentheses(calc):
    calc.add_to_expression("(")
    calc.add_to_expression(3)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.add_to_expression(")")
    calc.append_operator("*")
    calc.add_to_expression(5)
    calc.evaluate()
    assert calc.current_expression == "25"

def test_operator_precedence(calc):
    calc.add_to_expression(3)
    calc.append_operator("*")
    calc.add_to_expression(4)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.evaluate()
    assert calc.current_expression == "14"  # (3*4)+2 = 14

def test_negative_numbers(calc):
    calc.add_to_expression("-5")
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.evaluate()
    assert calc.current_expression == "-2"
def test_square_raises_exception():
    calc = CalculatorLogic()
    calc.current_expression = "abc"  # invalid input for eval
    calc.square()
    assert calc.get_current_expression() == "Error"

def test_sqrt_raises_exception_on_non_numeric():
    calc = CalculatorLogic()
    calc.current_expression = "xyz"  # invalid float conversion
    calc.sqrt()
    assert calc.get_current_expression() == "Error"

def test_sqrt_negative_number():
    calc = CalculatorLogic()
    calc.current_expression = "-9"  # valid number, but invalid for sqrt
    calc.sqrt()
    assert calc.get_current_expression() == "Error"