import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_evaluate_valid(calculator):
    calculator.expression = "2+3*4"
    assert calculator.evaluate() == "14"

def test_multiple_operations(calculator):
    calculator.expression = "2+3-1*5/2"
    assert calculator.evaluate() == str(eval("2+3-1*5/2"))

def test_parentheses(calculator):
    calculator.expression = "(2+3)*(4-2)"
    assert calculator.evaluate() == "10"

def test_operator_precedence(calculator):
    calculator.expression = "2+3*4"
    assert calculator.evaluate() == "14"

def test_parentheses_precedence(calculator):
    calculator.expression = "(2+3)*4"
    assert calculator.evaluate() == "20"

def test_nested_parentheses(calculator):
    calculator.expression = "((1+2)*3+(4/2))"
    assert calculator.evaluate() == "11.0"

def test_multiple_consecutive_operations(calculator):
    calculator.expression = "1+2-3+4-5+6"
    assert calculator.evaluate() == "5"

def test_expression_with_spaces(calculator):
    calculator.expression = "  2 + 3 *  4 "
    assert calculator.evaluate() == "14"

def test_expression_with_only_number(calculator):
    calculator.expression = "7"
    assert calculator.evaluate() == "7"

def test_evaluation_after_delete(calculator):
    calculator.expression = "12+34"
    calculator.delete()
    assert calculator.expression == "12+3"
    assert calculator.evaluate() == "15"
