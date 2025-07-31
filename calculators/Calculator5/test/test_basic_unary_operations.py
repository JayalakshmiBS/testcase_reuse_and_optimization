import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.calculator_logic import unary_operation

# Test case for sin operation
@pytest.mark.parametrize("a, expected", [
    ("90", 1.0),
    ("-30", -0.5)
])
def test_sin(a, expected):
    assert unary_operation(a, "sin") == pytest.approx(expected, rel=1e-2)

# Test case for cos operation
@pytest.mark.parametrize("a, expected", [
    ("0", 1.0),
    ("-60", 0.5)
])
def test_cos(a, expected):
    assert unary_operation(a, "cos") == pytest.approx(expected, rel=1e-2)

# Test case for square root operation
@pytest.mark.parametrize("a, expected", [
    ("16", 4.0),
    ("2", 1.41421),
    ("0", 0.0),
    ("1000000", 1000.0)
])
def test_square_root(a, expected):
    assert unary_operation(a, "√") == pytest.approx(expected, rel=1e-5)

# Test case for square operation
@pytest.mark.parametrize("a, expected", [
    ("4", 16.0),
    ("-3", 9.0)
])
def test_square(a, expected):
    assert unary_operation(a, "x²") == expected

# Test case for cube operation
@pytest.mark.parametrize("a, expected", [
    ("2", 8.0),
    ("-2", -8.0)
])
def test_cube(a, expected):
    assert unary_operation(a, "x³") == expected

# Test case for factorial operation
@pytest.mark.parametrize("a, expected", [
    ("5", 120),
    ("0", 1),
    ("1", 1)
])
def test_factorial(a, expected):
    assert unary_operation(a, "!") == expected

# Test case for log operation
@pytest.mark.parametrize("a, expected", [
    ("100", 2.0),
    ("10", 1.0),
    ("1", 0.0),
    ("1000000", 6.0),
    ("0.5", -0.3010),
    ("0.1", -1.0)
])
def test_log(a, expected):
    assert unary_operation(a, "log") == pytest.approx(expected, rel=1e-2)

# Test case for inverse operation
@pytest.mark.parametrize("a, expected", [
    ("4", 0.25),
    ("0.5", 2.0)
])
def test_inverse(a, expected):
    assert unary_operation(a, "1/x") == expected

# Test case for sin with negative angle
@pytest.mark.parametrize("a, expected", [
    ("-30", -0.5)
])
def test_sin_negative_angle(a, expected):
    assert unary_operation(a, "sin") == pytest.approx(expected, rel=1e-2)

# Test case for cos with negative angle
@pytest.mark.parametrize("a, expected", [
    ("-60", 0.5)
])
def test_cos_negative_angle(a, expected):
    assert unary_operation(a, "cos") == pytest.approx(expected, rel=1e-2)

# Test case for square root with decimal result
@pytest.mark.parametrize("a, expected", [
    ("2", 1.41421)
])
def test_square_root_decimal(a, expected):
    assert unary_operation(a, "√") == pytest.approx(expected, rel=1e-5)

# Test case for square operation with negative number
@pytest.mark.parametrize("a, expected", [
    ("-3", 9.0)
])
def test_square_negative(a, expected):
    assert unary_operation(a, "x²") == expected

# Test case for cube operation with negative number
@pytest.mark.parametrize("a, expected", [
    ("-2", -8.0)
])
def test_cube_negative(a, expected):
    assert unary_operation(a, "x³") == expected

# Test case for factorial of zero
@pytest.mark.parametrize("a, expected", [
    ("0", 1)
])
def test_factorial_zero(a, expected):
    assert unary_operation(a, "!") == expected

# Test case for log with decimal value
@pytest.mark.parametrize("a, expected", [
    ("10", 1.0)
])
def test_log_decimal(a, expected):
    assert unary_operation(a, "log") == pytest.approx(expected, rel=1e-5)

# Test case for inverse with decimal number
@pytest.mark.parametrize("a, expected", [
    ("0.5", 2.0)
])
def test_inverse_decimal(a, expected):
    assert unary_operation(a, "1/x") == expected

# Test case for factorial edge case with 1
@pytest.mark.parametrize("a, expected", [
    ("1", 1)
])
def test_factorial_edge_case(a, expected):
    assert unary_operation(a, "!") == expected

# Test case for log of 1
@pytest.mark.parametrize("a, expected", [
    ("1", 0.0)
])
def test_log_one(a, expected):
    assert unary_operation(a, "log") == expected

# Test case for square root of zero
@pytest.mark.parametrize("a, expected", [
    ("0", 0.0)
])
def test_square_root_zero(a, expected):
    assert unary_operation(a, "√") == expected

# Test case for log with large input
@pytest.mark.parametrize("a, expected", [
    ("1000000", 6.0)
])
def test_log_large_input(a, expected):
    assert unary_operation(a, "log") == pytest.approx(expected, rel=1e-1)

# Test case for square root with large number
@pytest.mark.parametrize("a, expected", [
    ("1000000", 1000.0)
])
def test_square_root_large_number(a, expected):
    assert unary_operation(a, "√") == expected

# Test case for log with a fractional input
@pytest.mark.parametrize("a, expected", [
    ("0.5", -0.3010)
])
def test_log_fraction(a, expected):
    assert unary_operation(a, "log") == pytest.approx(expected, rel=1e-4)

# Test case for log between 0 and 1
@pytest.mark.parametrize("a, expected", [
    ("0.1", -1.0)
])
def test_log_between_zero_and_one(a, expected):
    assert unary_operation(a, "log") == pytest.approx(expected, rel=1e-1)

# Test case for log with very large input
@pytest.mark.parametrize("a, expected", [
    ("1000000000", 9.0)
])
def test_log_large_input(a, expected):
    assert unary_operation(a, "log") == pytest.approx(expected, rel=1e-1)
