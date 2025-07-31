import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic

def test_delete_after_result():
    calc = CalculatorLogic()
    calc.insert('2+3')
    calc.calculate()
    calc.delete_last()
    assert calc.expression == ''


def test_operator_after_result_keeps_previous_result():
    calc = CalculatorLogic()
    calc.insert("2+3")
    calc.calculate()  # Sets result_shown = True
    calc.insert("+")
    assert calc.expression == "5+"


def test_continue_after_result():
    calc = CalculatorLogic()
    calc.insert("2")
    calc.insert("+")
    calc.insert("3")
    calc.calculate()  # Should result in 5
    calc.insert("+")
    calc.insert("4")
    assert calc.expression == "5+4"


def test_operator_after_result_with_follow_up_expression():
    calc = CalculatorLogic()
    calc.insert('4*5')
    calc.calculate()  # Result is 20
    calc.insert('+')
    calc.insert('6')
    result = calc.calculate()
    assert result == '26'


def test_insert_after_incomplete_expression():
    calc = CalculatorLogic()
    calc.insert('2+')
    calc.insert('3')
    result = calc.calculate()
    assert result == '5'


def test_delete_insert_cycle():
    calc = CalculatorLogic()
    calc.insert('45')
    calc.delete_last()  # Becomes '4'
    calc.insert('6')    # Becomes '46'
    result = calc.calculate()
    assert result == '46'


def test_calculate_then_delete_then_continue():
    calc = CalculatorLogic()
    calc.insert('7+3')
    calc.calculate()        # Result is 10
    calc.delete_last()      # Clears expression
    calc.insert('2')        # New expression
    result = calc.calculate()
    assert result == '2'
