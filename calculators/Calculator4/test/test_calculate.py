import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcul_logic import calculate


def test_valid_operations():
    assert calculate('1', values=[1, 2]) == 3  # add
    assert calculate('2', values=[5, 2]) == 3  # subtract
    assert calculate('3', values=[2, 3]) == 6  # multiply
    assert calculate('4', x=6, y=2) == 3       # divide
    assert calculate('5', x=10, y=3) == 1      # modulus
    result = calculate('6', x=30)
    assert result == pytest.approx( 0.5, rel=1e-4)
    result = calculate('7', x=0)
    assert result == pytest.approx(1.0, rel=1e-4)



@pytest.mark.parametrize("option", ['9', 'invalid', None])
def test_invalid_operations(option):
    assert calculate(option) == "Invalid option"


def test_missing_parameters():
    with pytest.raises(TypeError):
        calculate('1')  # add missing values
    with pytest.raises(TypeError):
        calculate('4', x=2)  # divide missing y
    with pytest.raises(TypeError):
        calculate('4', y=2)  # divide missing x


def test_invalid_parameter_types():
    with pytest.raises(TypeError):
        calculate('1', values="not a list")  # add with string
    with pytest.raises(TypeError):
        calculate('4', x="10", y="2")  # divide with strings
