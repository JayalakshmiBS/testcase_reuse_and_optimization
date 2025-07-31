import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.calculator_logic import binary_operation

# Parametrize the addition operation
@pytest.mark.parametrize("a, b, expected", [
    ("5", "3", 8.0),
    ("10", "4", 14.0),
    ("5.5", "3.2", 8.7),
    ("-1", "-3", -4.0),
    ("10", "-3", 7.0),
])
def test_addition(a, b, expected):
    assert binary_operation(a, b, "+") == expected

# Parametrize the subtraction operation
@pytest.mark.parametrize("a, b, expected", [
    ("10", "4", 6.0),
    ("6", "7", -1.0),
    ("3", "10", -7.0),
    ("-5", "-5", 0.0),
    ("5.5", "3", 2.5),
])
def test_subtraction(a, b, expected):
    assert binary_operation(a, b, "-") == expected

# Parametrize the multiplication operation
@pytest.mark.parametrize("a, b, expected", [
    ("6", "7", 42.0),
    ("5", "0", 0.0),
    ("-2", "3", -6.0),
    ("1.5", "2.0", 3.0),
    ("-1", "-5", 5.0),
])
def test_multiplication(a, b, expected):
    assert binary_operation(a, b, "*") == expected

# Parametrize the division operation
@pytest.mark.parametrize("a, b, expected", [
    ("8", "2", 4.0),
    ("1", "3", 0.333),  # Dividing decimals
    ("5", "2", 2.5),
    ("10", "-2", -5.0),
    ("-10", "2", -5.0),
    ("5", "0", "Error"),  # Handling divide by zero
])
def test_division(a, b, expected):
    if expected == "Error":
        assert binary_operation(a, b, "/") == expected
    else:
        assert binary_operation(a, b, "/") == pytest.approx(expected, abs=1e-3)

# Parametrize the modulus operation
@pytest.mark.parametrize("a, b, expected", [
    ("10", "3", 1.0),
    ("5.5", "3", 2.5),
    ("-5", "3", 1.0),
    ("-10", "-3", -1.0),
    ("5", "0", "Error"),  # Handling modulus by zero
])
def test_modulus(a, b, expected):
    if expected == "Error":
        assert binary_operation(a, b, "%") == expected
    else:
        assert binary_operation(a, b, "%") == expected

# Parametrize the exponentiation operation
@pytest.mark.parametrize("a, b, expected", [
    ("2", "3", 8.0),
    ("4", "0.5", 2.0),
    ("-2", "3", -8.0),
    ("5", "0", 1.0),
    ("2.5", "3", 15.625),
    ("-3", "2", 9.0),
])
def test_exponentiation(a, b, expected):
    assert binary_operation(a, b, "^") == pytest.approx(expected, abs=1e-3)

# Additional test cases

# Test for floating point division precision
@pytest.mark.parametrize("a, b, expected", [
    ("1", "3", 0.333),  # Dividing decimals
])
def test_division_with_decimals(a, b, expected):
    assert binary_operation(a, b, "/") == pytest.approx(expected, abs=1e-3)

# Parametrize additional edge cases
@pytest.mark.parametrize("a, b, expected", [
    ("1000000000000", "5000000000000", 6000000000000.0),
    ("-1000000000000", "-5000000000000", -6000000000000.0),
    ("123456.789", "987654.321", 1111111.11),
])
def test_large_numbers(a, b, expected):
    assert binary_operation(a, b, "+") == expected

# Test for exponentiation with fractional base
@pytest.mark.parametrize("a, b, expected", [
    ("2.5", "3", 15.625),
])
def test_exponentiation_float_base(a, b, expected):
    assert binary_operation(a, b, "^") == pytest.approx(expected, abs=1e-3)

# Test for invalid inputs and edge cases
@pytest.mark.parametrize("a, b, expected", [
    ("5", "0", "Error"),  # Division by zero
    ("5", "0", "Error"),  # Modulus by zero
])
def test_invalid_operations(a, b, expected):
    assert binary_operation(a, b, "/") == expected
    assert binary_operation(a, b, "%") == expected
