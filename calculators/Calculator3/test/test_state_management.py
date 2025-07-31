import sys
import os
import pytest

# Ensure parent directory is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_clear_after_evaluation(calculator):
    calculator.expression = "3+3"
    calculator.evaluate()
    calculator.clear()
    assert calculator.expression == ""

def test_state_after_evaluate_then_click(calculator):
    calculator.expression = "2+2"
    calculator.evaluate()
    calculator.click_button("+3")
    assert calculator.expression == "4+3"

def test_state_reset_on_error(calculator):
    calculator.expression = "10/0"
    calculator.evaluate()
    assert calculator.expression == ""
    calculator.click_button("5")
    assert calculator.expression == "5"
