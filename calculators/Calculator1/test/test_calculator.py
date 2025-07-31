import pytest
import sys
import os,math
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.calc_logic import CalculatorLogic


@pytest.fixture
def calc():
    return CalculatorLogic()

def test_decimal_button(calc):
    calc.add_to_expression(7)
    calc.add_to_expression(".")
    calc.add_to_expression(5)
    assert calc.current_expression == "7.5"

def test_operator_button(calc):
    calc.add_to_expression(3)
    calc.append_operator("+")
    assert calc.current_expression == ""
    assert calc.total_expression == "3+"

def test_multiple_operator_buttons(calc):
    calc.add_to_expression(5)
    calc.append_operator("+")
    calc.add_to_expression(3)
    calc.append_operator("*")
    calc.add_to_expression(2)
    calc.evaluate()
    assert calc.current_expression == "11"

# def test_clear_button(calc):
#     calc.add_to_expression(4)
#     calc.append_operator("+")
#     calc.add_to_expression(5)
#     calc.clear()
#     assert calc.current_expression == ""
#     assert calc.total_expression == ""

def test_square_button(calc):
    calc.add_to_expression(4)
    calc.square()
    assert calc.current_expression == "16"

def test_sqrt_button(calc):
    calc.add_to_expression(16)
    calc.sqrt()
    assert calc.current_expression == "4.0"

def test_evaluate_basic(calc):
    calc.add_to_expression(2)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.evaluate()
    assert calc.current_expression == "4"

def test_evaluate_invalid_expression(calc):
    calc.add_to_expression(5)
    calc.append_operator("/")
    calc.add_to_expression(0)
    calc.evaluate()
    assert calc.current_expression == "Error"

# def test_total_label_update(calc):
#     calc.add_to_expression('7')
#     calc.append_operator('+')
#     calc.add_to_expression('3')
#     calc.update_total_label()
#     assert calc.total_label.cget("text") == "7 + "

# def test_long_input_display(calc):
#     for _ in range(11):
#         calc.add_to_expression('9')
#     assert calc.current_expression == "99999999999"
#     assert calc.label.cget("text") == "99999999999"

def test_ui_update_after_calculation(calc):
    calc.add_to_expression(8)
    calc.append_operator("+")
    calc.add_to_expression(2)
    calc.evaluate()
    assert calc.current_expression == "10"
    assert calc.total_expression == ""
