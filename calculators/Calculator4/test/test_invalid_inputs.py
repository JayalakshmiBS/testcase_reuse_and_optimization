import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import calculate, add, divide


def test_calculate_invalid_type_choice():
    assert calculate(None) == "Invalid option"


def test_calculate_invalid_string_choice():
    assert calculate('invalid') == "Invalid option"


def test_add_with_strings():
    with pytest.raises(TypeError):
        add(["a", "b"])


def test_divide_with_string_input():
    with pytest.raises(TypeError):
        divide("10", "2")
