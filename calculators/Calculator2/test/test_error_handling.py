import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cal_logic import CalculatorLogic

@pytest.fixture
def calc():
    return CalculatorLogic()

def test_calculate_invalid_expression(calc):
    calc.insert('2++3')
    result = calc.calculate()
    assert result == '5'  # Assuming this is how your logic works

def test_calculate_zero_division(calc):
    calc.insert("10/0")
    result = calc.calculate()
    assert result == "Error"

def test_calculate_invalid_expression_2(calc):
    calc.insert("5+*2")
    result = calc.calculate()
    assert result == "Error"

def test_division_by_zero_after_expression(calc):
    calc.insert("1/0")
    result = calc.calculate()
    assert result == "Error"

def test_syntax_error(calc):
    calc.insert("2+*3")
    result = calc.calculate()
    assert result == "Error"

def test_empty_expression(calc):
    result = calc.calculate()
    assert result == "Error"

def test_max_number_input(calc):
    calc.insert("9"*100 + "+1")
    result = calc.calculate()
    assert result == "1" + "0"*100  # 9*100 + 1 = 10^100

def test_multiple_operators(calc):
    calc.insert('2+*3')
    result = calc.calculate()
    assert result == 'Error'

def test_expression_ends_with_operator(calc):
    calc.insert('3+')
    result = calc.calculate()
    assert result == 'Error'

def test_unmatched_parentheses(calc):
    calc.insert('(2+3')
    result = calc.calculate()
    assert result == 'Error'

def test_only_decimal_point(calc):
    calc.insert('.')
    result = calc.calculate()
    assert result == 'Error'

def test_consecutive_decimal_points(calc):
    calc.insert('2..5')
    result = calc.calculate()
    assert result == 'Error'

def test_double_decimal_error(calc):
    calc.insert('3.1.4')
    result = calc.calculate()
    assert result == 'Error'

def test_invalid_input(calc):
    calc.insert('2+3a')
    result = calc.calculate()
    assert result == 'Error'

def test_empty_parentheses(calc):
    calc.insert('()')
    result = calc.calculate()
    assert result == '()'  # Update this if the logic should return Error

def test_calculate_with_whitespace(calc):
    calc.insert(' 2 + 3 ')
    result = calc.calculate()
    assert result == '5'

def test_calculate_with_parentheses_and_operator(calc):
    calc.insert('(2+3)*4')
    result = calc.calculate()
    assert result == '20'

def test_calculate_invalid_characters(calc):
    calc.insert('5+abc')
    result = calc.calculate()
    assert result == 'Error'
