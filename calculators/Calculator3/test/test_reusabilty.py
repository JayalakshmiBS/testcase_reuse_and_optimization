import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_repeated_evaluation_same_result(calculator):
    calculator.expression = "2*5"
    result1 = calculator.evaluate()
    result2 = calculator.evaluate()
    assert result1 == "10"
    assert result2 == "10"
