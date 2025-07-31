import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calculator_logic import binary_operation, unary_operation


def test_multiple_whitespaces_input():
    assert binary_operation("  5  ", "  3  ", "+") == 8.0
    assert unary_operation("  16  ", "√") == 4.0

def test_whitespace_in_input():
    assert binary_operation(" 5 ", " 3 ", "+") == 8.0
    assert unary_operation(" 16 ", "√") == 4.0

def test_leading_zeros_input():
    assert binary_operation("05", "03", "+") == 8.0
    assert unary_operation("016", "√") == 4.0

def test_multiple_whitespaces_unary():
    assert unary_operation("   4   ", "√") == 2.0
