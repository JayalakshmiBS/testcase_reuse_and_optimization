import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calcu_logic import CalculatorLogic

@pytest.fixture
def calculator():
    return CalculatorLogic()

def test_evaluate(calculator):
    calculator.click_button('2+3*4')
    result = calculator.evaluate()
    assert result == '14'
