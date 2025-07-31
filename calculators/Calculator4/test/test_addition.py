import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import normally
from src.calcul_logic import add


def test_add_positive_numbers():
    assert add([1, 2, 3]) == 6
    assert add([10, 20, 30]) == 60

def test_add_negative_numbers():
    assert add([-1, -2, -3]) == -6
    assert add([-10, -20]) == -30

def test_add_mixed_numbers():
    assert add([-1, 2, -3, 4]) == 2
    assert add([10, -5, 3]) == 8

def test_add_floats():
    assert add([1.5, 2.5]) == pytest.approx(4.0)
    assert add([0.1, 0.2]) == pytest.approx(0.3, rel=1e-1)

def test_add_empty_list():
    assert add([]) == 0

def test_add_large_numbers():
    assert add([1e10, 1e10]) == 2e10

def test_add_invalid_types():
    with pytest.raises(TypeError):
        add(["a", "b"])
    with pytest.raises(TypeError):
        add([1, "2"])
