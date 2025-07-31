
# import sys
# import os,math
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from calc import Calculator

# import pytest


# @pytest.fixture
# def calc():
#     return Calculator()

# def test_memory_store_and_recall(calc):
#     calc.add_to_expression(5)
#     calc.memory_store()
#     calc.clear()
#     calc.memory_recall()
#     assert calc.current_expression == "5"

# def test_memory_clear(calc):
#     calc.add_to_expression(7)
#     calc.memory_store()
#     calc.memory_clear()
#     calc.memory_recall()
#     assert calc.current_expression == "0"

# def test_memory_after_calculation(calc):
#     calc.add_to_expression(10)
#     calc.append_operator("+")
#     calc.add_to_expression(20)
#     calc.evaluate()
#     calc.memory_store()
#     calc.clear()
#     calc.memory_recall()
#     assert calc.current_expression == "30"
