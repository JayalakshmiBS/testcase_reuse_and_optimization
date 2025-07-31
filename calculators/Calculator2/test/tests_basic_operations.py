import pytest
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cal_logic import CalculatorLogic

@pytest.fixture
def calc():
    return CalculatorLogic()


def test_insert_basic(calc):
    calc.insert('1')
    assert calc.expression == '1'


def test_float_leading_decimal(calc):
    calc.insert('.5 + .5')
    assert calc.calculate() == '1.0'


def test_multiple_operations(calc):
    calc.insert('2 + 3 * 4')
    assert calc.calculate() == '14'


def test_insert_after_result():
    logic = CalculatorLogic()
    logic.expression = "5"
    logic.result_shown = True
    assert logic.insert("2") == "2"
    logic.result_shown = True
    assert logic.insert("+") == "2+"


def test_leading_zero_handling():
    logic = CalculatorLogic()
    logic.insert("0")
    logic.insert("5")
    assert logic.expression == "5"


def test_delete_last_character():
    logic = CalculatorLogic()
    logic.insert("123")
    logic.delete_last()
    assert logic.expression == "12"


def test_cancel_resets_state():
    logic = CalculatorLogic()
    logic.insert("99")
    logic.cancel()
    assert logic.expression == ""
    assert not logic.result_shown


def test_calculate_basic_expression():
    logic = CalculatorLogic()
    logic.insert("2")
    logic.insert("+")
    logic.insert("3")
    result = logic.calculate()
    assert result == "5"
    assert logic.result_shown


def test_chained_operations(calc):
    calc.insert("2+3")
    calc.calculate()
    calc.insert("*")
    calc.insert("4")
    assert calc.calculate() == "20"


def test_cancel_empty_expression(calc):
    result = calc.cancel()
    assert result == ""
    assert not calc.result_shown


def test_cancel_after_input(calc):
    calc.expression = "123"
    result = calc.cancel()
    assert result == ""
    assert not calc.result_shown


def test_decimal_edge_case_path(calc):
    calc.insert("2.5+")
    calc.insert("3..5")
    assert calc.calculate() == "Error"


def test_insert_operator_after_result(calc):
    calc.insert("2+3")
    calc.calculate()
    calc.insert("+")
    assert calc.expression == "5+"


def test_cancel(calc):
    calc.insert('1')
    calc.cancel()
    assert calc.expression == ''


def test_delete_last(calc):
    calc.insert('12')
    calc.delete_last()
    assert calc.expression == '1'


def test_delete_last_empty(calc):
    calc.delete_last()
    assert calc.expression == ''


def test_consecutive_deletions(calc):
    calc.insert('123')
    calc.delete_last()
    calc.delete_last()
    calc.delete_last()
    assert calc.expression == ''


def test_empty_then_insert(calc):
    assert calc.expression == ''
    calc.insert('9')
    assert calc.expression == '9'


def test_insert_after_multiple_cancels(calc):
    calc.insert('123')
    calc.cancel()
    calc.insert('4')
    result = calc.calculate()
    assert result == '4'
