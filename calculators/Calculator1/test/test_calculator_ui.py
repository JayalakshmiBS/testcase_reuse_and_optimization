# import unittest
# import sys
# import os,math
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from calc import Calculator

# class TestCalculatorUI(unittest.TestCase):
    
#     def test_button_creation(self):
#         # Check if all buttons are created
#         calc = Calculator()
        
#         # Test digit buttons
#         for digit in calc.digits:
#             button = calc.buttons_frame.nametowidget(calc.digits[digit])
#             self.assertIsNotNone(button)
        
#         # Test operator buttons
#         for operator in calc.operations:
#             button = calc.buttons_frame.nametowidget(calc.operations[operator])
#             self.assertIsNotNone(button)
    
#     def test_ui_update_after_calculation(self):
#         # Test if the UI updates correctly after calculation
#         calc = Calculator()
#         calc.add_to_expression(4)
#         calc.append_operator("+")
#         calc.add_to_expression(5)
#         calc.evaluate()
#         self.assertEqual(calc.current_expression, "9")
#         self.assertEqual(calc.total_expression, "")

# if __name__ == "__main__":
#     unittest.main()
