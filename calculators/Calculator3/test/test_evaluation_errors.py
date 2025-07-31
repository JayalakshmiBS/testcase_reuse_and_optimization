import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_evaluate_zero_division(calculator):
    calculator.expression = "10/0"
    assert calculator.evaluate() == "Error"
    assert calculator.expression == ""

def test_evaluate_invalid(calculator):
    calculator.expression = "5++"
    assert calculator.evaluate() == "Error"
    assert calculator.expression == ""

def test_evaluate_invalid_expression(calculator):
    calculator.click_button('5/0')
    result = calculator.evaluate()
    assert result == "Error"

def test_empty_expression_evaluation(calculator):
    calculator.expression = ""
    assert calculator.evaluate() == "Error"

def test_expression_ends_with_operator(calculator):
    calculator.expression = "5+"
    assert calculator.evaluate() == "Error"

def test_expression_with_only_operator(calculator):
    calculator.expression = "+"
    assert calculator.evaluate() == "Error"

def test_invalid_type_mix(calculator):
    calculator.expression = "'5'+5"
    assert calculator.evaluate() == "Error"

def test_clear_then_evaluate(calculator):
    calculator.expression = "2+2"
    calculator.clear()
    assert calculator.evaluate() == "Error"
