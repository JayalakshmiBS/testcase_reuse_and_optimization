import pytest
import sys
import os,math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calc_logic import CalculatorLogic


@pytest.fixture
def calc():
    return CalculatorLogic()

def test_square_button(calc):
    calc.add_to_expression(5)
    calc.square()
    assert calc.current_expression == "25"

def test_sqrt_button(calc):
    calc.add_to_expression(9)
    calc.sqrt()
    assert calc.current_expression == "3.0"

def test_clear_button(calc):
    calc.add_to_expression(5)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.clear()
    assert calc.current_expression == ""
    assert calc.total_expression == ""

def test_equals_button(calc):
    calc.add_to_expression(5)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.evaluate()
    assert calc.current_expression == "8"
