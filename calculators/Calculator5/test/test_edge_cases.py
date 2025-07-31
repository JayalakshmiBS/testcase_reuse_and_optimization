import sys
import os,pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from src.calculator_logic import binary_operation

@pytest.mark.parametrize("a,b,expected",[
    ("123456.789", "987654.321",1111111.11)
])
def test_large_decimal_result(a,b,expected):
    assert binary_operation(a,b, "+") == expected

