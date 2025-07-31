import pytest
import sys
import os, math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calc_logic import CalculatorLogic

@pytest.fixture
def calc():
    return CalculatorLogic()

def test_empty_input_on_evaluate(calc):
    calc.evaluate()
    assert calc.current_expression == "Error"

def test_invalid_square_root(calc):
    calc.add_to_expression(-9)
    calc.sqrt()
    assert calc.current_expression == "Error"

def test_long_input_display(calc):
    for _ in range(5):
        calc.add_to_expression(7)
    assert calc.current_expression == "77777"
    assert calc.get_current_expression() == "77777"  # Replace get_display_text with get_current_expression

def test_display_truncation(calc):
    for _ in range(12):  # Adds 12 sevens
        calc.add_to_expression(7)
    assert calc.current_expression == "777777777777"
    assert calc.get_current_expression() == "77777777777"  # Only first 11 characters
