import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic


@pytest.fixture
def calc():
    return CalculatorLogic()


def test_click_button_basic(calc):
    calc.click_button('2')
    assert calc.expression == '2'


def test_click_non_numeric_characters(calc):
    calc.click_button("+")
    calc.click_button("-")
    calc.click_button("*")
    assert calc.expression == "+-*"


def test_clear(calc):
    calc.click_button(5)
    assert calc.clear() == ""
    assert calc.expression == ""


def test_delete(calc):
    calc.expression = "123"
    assert calc.delete() == "12"
    assert calc.delete() == "1"
    assert calc.delete() == ""
    assert calc.delete() == ""


def test_delete_after_clear(calc):
    calc.click_button("9")
    calc.clear()
    assert calc.delete() == ""


def test_delete_on_single_character(calc):
    calc.expression = "9"
    calc.delete()
    assert calc.expression == ""


def test_delete_on_expression_result(calc):
    calc.expression = "3+3"
    calc.evaluate()
    calc.delete()
    assert calc.expression == ""


def test_multiple_deletes(calc):
    calc.expression = "123456"
    for _ in range(3):
        calc.delete()
    assert calc.expression == "123"


def test_multiple_deletes_to_empty(calc):
    calc.expression = "98765"
    for _ in range(5):
        calc.delete()
    assert calc.expression == ""


def test_clear_works_with_empty_expression(calc):
    calc.expression = ""
    calc.clear()
    assert calc.expression == ""


def test_multiple_clear_calls(calc):
    calc.expression = "123"
    calc.clear()
    assert calc.expression == ""
    calc.clear()
    assert calc.expression == ""
