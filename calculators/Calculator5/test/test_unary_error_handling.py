import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calculator_logic import unary_operation


def test_inverse_zero():
    assert unary_operation("0", "1/x") == "Error"

def test_factorial_float_input():
    assert unary_operation("5.5", "!") == "Error"

def test_log_zero():
    assert unary_operation("0", "log") == "Error"

def test_root_negative():
    assert unary_operation("-4", "√") == "Error"

def test_unknown_unary_func():
    assert unary_operation("5", "cot") == "Unknown"

def test_invalid_unary_input():
    assert unary_operation("a", "sin") == "Error"

def test_factorial_negative_input():
    assert unary_operation("-5", "!") == "Error"

def test_log_negative_input():
    assert unary_operation("-1", "log") == "Error"

def test_factorial_of_decimal():
    assert unary_operation("2.5", "!") == "Error"

def test_factorial_large_number():
    assert unary_operation("171", "!") == "Too Large"

def test_negative_input_log():
    assert unary_operation("-10", "log") == "Error"

def test_factorial_greater_than_170():
    assert unary_operation("171", "!") == "Too Large"

def test_factorial_non_integer():
    assert unary_operation("5.1", "!") == "Error"

def test_empty_string_unary():
    assert unary_operation("", "sin") == "Error"

def test_unary_non_numeric_input():
    assert unary_operation("abc", "sin") == "Error"

def test_factorial_max_input():
    assert unary_operation("170", "!") == "Too Large"

def test_factorial_overflow():
    assert unary_operation("10000", "!") == "Too Large"

def test_error_propagation_unary():
    assert unary_operation("-1", "!") == "Error"
    assert unary_operation("-1", "log") == "Error"
    assert unary_operation("-1", "√") == "Error"

def test_factorial_large_float():
    assert unary_operation("170.5", "!") == "Error"

def test_factorial_of_zero():
    assert unary_operation("0", "!") == 1
