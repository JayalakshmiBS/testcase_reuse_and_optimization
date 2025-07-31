import sys
import os
import math
import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calc_logic import CalculatorLogic

@pytest.fixture
def calc():
    return CalculatorLogic()

def test_path_add_then_multiply(calc):
    calc.add_to_expression(1)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.append_operator("*")
    calc.add_to_expression(3)
    calc.evaluate()
    assert calc.current_expression == "7"

def test_path_parentheses(calc):
    calc.add_to_expression("(")
    calc.add_to_expression(1)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.add_to_expression(")")
    calc.append_operator("*")
    calc.add_to_expression(3)
    calc.evaluate()
    assert calc.current_expression == "9"

def test_operator_overwrite(calc):
    calc.add_to_expression(1)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.append_operator("-")
    calc.add_to_expression(3)
    calc.evaluate()
    assert calc.current_expression == "0"

def test_square_root(calc):
    calc.add_to_expression(9)
    calc.sqrt()
    assert calc.current_expression == "3.0"

def test_square_root_zero(calc):
    calc.add_to_expression(0)
    calc.sqrt()
    assert calc.current_expression == "0.0"

def test_square_root_negative(calc):
    calc.add_to_expression(-9)
    calc.sqrt()
    assert calc.current_expression == "Error"

def test_square(calc):
    calc.add_to_expression(4)
    calc.square()
    assert calc.current_expression == "16"

def test_square_zero(calc):
    calc.add_to_expression(0)
    calc.square()
    assert calc.current_expression == "0"

def test_zero_division(calc):
    calc.add_to_expression(5)
    calc.append_operator("/")
    calc.add_to_expression(0)
    calc.evaluate()
    assert calc.current_expression == "Error"

def test_parentheses_expression(calc):
    calc.add_to_expression("(")
    calc.add_to_expression(2)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.add_to_expression(")")
    calc.append_operator("*")
    calc.add_to_expression(4)
    calc.evaluate()
    assert calc.current_expression == "20"

def test_multiple_decimal_points(calc):
    calc.add_to_expression(3)
    calc.append_operator(".")
    calc.add_to_expression(5)
    calc.append_operator(".")
    calc.add_to_expression(7)
    assert calc.current_expression == "7"

def test_multiple_operations(calc):
    calc.add_to_expression(2)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.append_operator("*")
    calc.add_to_expression(4)
    calc.evaluate()
    assert calc.current_expression == "14"

def test_long_expression(calc):
    calc.add_to_expression(12)
    calc.append_operator("+")
    calc.add_to_expression(34)
    calc.append_operator("*")
    calc.add_to_expression(56)
    calc.append_operator("/")
    calc.add_to_expression(78)
    calc.append_operator("-")
    calc.add_to_expression(90)
    calc.evaluate()
    assert calc.current_expression == "-53.58974358974359"

def test_clear_function(calc):
    calc.add_to_expression(5)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.clear()
    assert calc.current_expression == ""

def test_error_recovery_invalid_expression(calc):
    calc.add_to_expression(5)
    calc.append_operator("+")
    calc.add_to_expression("+")
    calc.evaluate()
    assert calc.current_expression == "Error"
