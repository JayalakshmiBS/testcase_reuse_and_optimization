import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import divide

@pytest.mark.parametrize(
    "x, y, expected",
    [
        (10, 2, 5),
        (100, 10, 10),
    ]
)
def test_divide_positive_numbers(x, y, expected):
    assert divide(x, y) == expected


@pytest.mark.parametrize(
    "x, y, expected, tolerance",
    [
        (5.5, 2.2, 2.5, 1e-1),
        (1.0, 3.0, 0.333333, 1e-5)  # relaxed tolerance

    ]
)
def test_divide_floats(x, y, expected, tolerance):
    assert divide(x, y) == pytest.approx(expected, rel=tolerance)


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (-10, 2, -5),
        (10, -2, -5),
        (-10, -2, 5),
    ]
)
def test_divide_negative_numbers(x, y, expected):
    assert divide(x, y) == expected


def test_divide_by_zero():
    assert divide(5, 0) == "Cannot divide by zero"


@pytest.mark.parametrize(
    "x, y",
    [
        ("10", "2"),
        (10, "2"),
    ]
)
def test_divide_invalid_types(x, y):
    with pytest.raises(TypeError):
        divide(x, y)
