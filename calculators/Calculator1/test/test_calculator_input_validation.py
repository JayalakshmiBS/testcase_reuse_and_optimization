import pytest
import sys
import os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calc_logic import CalculatorLogic


@pytest.fixture
def calc():
    return CalculatorLogic()

def test_invalid_character(calc):
    calc.add_to_expression("a")
    # Assuming Calculator allows the character to be part of the expression
    assert calc.current_expression == "a"

def test_empty_expression(calc):
    calc.evaluate()
    assert calc.current_expression == "Error"

def test_multiple_operators(calc):
    calc.add_to_expression(5)
    calc.append_operator("+")
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.evaluate()
    assert calc.current_expression == "8"  # Or handle expected error if "+"+ is not valid
