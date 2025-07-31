import os
import sys
import pytest
import math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calc_logic import CalculatorLogic
 # Make sure this matches the actual module and class name

@pytest.fixture
def calc():
    return CalculatorLogic()

@pytest.mark.parametrize("val1, op, val2, expected", [
    (5, "+", 3, "8"),
    (2, "*", 4, "8"),
    (10, "-", 6, "4"),
    (20, "/", 4, "5.0"),
    (9, "%", 4, "1"),
    (7, "-", 7, "0"),
    (0, "+", 0, "0"),
    (100, "*", 0, "0"),
    (-5, "+", 10, "5"),
])
def test_arithmetic_operations(calc, val1, op, val2, expected):
    calc.clear()
    calc.add_to_expression(val1)
    calc.append_operator(op)
    calc.add_to_expression(val2)
    calc.evaluate()
    assert calc.get_current_expression() == expected


def test_clear(calc):
    calc.add_to_expression(10)
    calc.total_expression = "something"
    calc.clear()
    assert calc.current_expression == ""
    assert calc.total_expression == ""


def test_square_operation(calc):
    calc.add_to_expression(5)
    calc.square()
    assert calc.current_expression == "25"

    calc.clear()
    calc.add_to_expression(0)
    calc.square()
    assert calc.current_expression == "0"


def test_sqrt_operation(calc):
    calc.add_to_expression(16)
    calc.sqrt()
    assert calc.current_expression == "4.0"

    calc.clear()
    calc.add_to_expression(0)
    calc.sqrt()
    assert calc.current_expression == "0.0"

    calc.clear()
    calc.add_to_expression(-9)
    calc.sqrt()
    assert calc.current_expression == "Error"


def test_invalid_expressions(calc):
    calc.current_expression = "5++"
    calc.evaluate()
    assert calc.current_expression == "Error"

    calc.clear()
    calc.total_expression = "10/0"
    calc.evaluate()
    assert calc.current_expression == "Error"


def test_chained_expression(calc):
    calc.add_to_expression(2)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.append_operator("*")
    calc.add_to_expression(4)
    calc.evaluate()
    assert calc.get_current_expression() == "14"  # 2 + (3*4)


def test_getters(calc):
    calc.add_to_expression(1234567890123456)
    assert calc.get_current_expression() == "12345678901"
    calc.append_operator("+")
    assert "+" in calc.get_total_expression()
