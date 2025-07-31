import sys
import os
import unittest
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calculator_logic import binary_operation



@pytest.mark.parametrize("a, b, expected", [
        ("8", "0", "Error"), 
        ("0","0","Error"), # Division by zero
    ])
def test_division_by_zero( a, b, expected):
        assert binary_operation(a, b, "/") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("4", "2", "Invalid"),  # Invalid operator
    ])
def test_invalid_binary_op( a, b, expected):
        assert binary_operation(a, b,  "&") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("a", "2", "Error"),  # Invalid input (non-numeric)
    ])
def test_invalid_binary_input( a, b, expected):
        assert binary_operation(a, b, "+") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("", "5", "Error"),  # Empty input
        ("5", "", "Error"),  # Empty input
    ])
def test_empty_input_binary( a, b, expected):
        assert binary_operation(a, b,  "+") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("0", "-5", "Error"),  # Invalid exponentiation with zero base
    ])
def test_zero_base_negative_exponent( a, b, expected):
        assert binary_operation(a, b, "^") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("five", "3", "Error"),  # Non-numeric string
    ])
def test_addition_with_string_input( a, b, expected):
        assert binary_operation(a, b, "+") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("abc", "123", "Error"),  # Non-numeric string
    ])
def test_binary_with_non_numeric_strings( a, b, expected):
        assert binary_operation(a, b, "+") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("2", "100",  1.2676506002282295e+30),  # Large exponentiation
    ])
def test_large_exponentiation( a, b, expected):
        assert binary_operation(a, b, "^") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("0", "5", 0.0),  # Zero exponentiation
    ])
def test_zero_exponentiation( a, b, expected):
        assert binary_operation(a, b, "^") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("999999", "100", "Error"),  # Large exponentiation that overflows
    ])
def test_large_exponentiation_result(a, b, expected):
        assert binary_operation(a, b, "^") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("5", "3", "Invalid"),  # Multiple operators
    ])
def test_multiple_operators( a, b,expected):
        assert binary_operation(a, b, "+-") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("1,000", "500", "Error"),  # Invalid number format
    ])
def test_inconsistent_number_format( a, b , expected):
        assert binary_operation(a, b, "+") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("abc", "2", "Error"),  # Non-numeric string
        ("2", "abc", "Error"),  # Non-numeric string
    ])
def test_error_propagation_binary( a, b, expected):
        assert binary_operation(a, b, "+") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("2", "-3", 0.125),  # Negative exponentiation
    ])
def test_negative_exponentiation( a, b, expected):
        assert binary_operation(a, b, "^") == expected

@pytest.mark.parametrize("a, b, expected", [
        ("0", "5", 0.0),  # Zero exponentiation
    ])
def test_zero_exponentiation( a, b, expected):
        assert binary_operation(a, b, "^") == expected
