import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cal_logic import CalculatorLogic

@pytest.fixture
def calc():
    return CalculatorLogic()

def test_invalid_decimal_input(calc):
    calc.insert("3.14.15")
    result = calc.calculate()
    assert result == "Error"

def test_float_addition(calc):
    calc.insert('2.5+3.5')
    result = calc.calculate()
    assert result == '6.0'

def test_float_division(calc):
    calc.insert('5.0/2.0')
    result = calc.calculate()
    assert result == '2.5'

def test_insert_number_after_decimal_point(calc):
    calc.insert('.')
    calc.insert('5')
    assert calc.expression == '.5'
