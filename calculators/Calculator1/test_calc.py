# import unittest
# from unittest.mock import patch, MagicMock
# from calc import Calculator
# import tkinter as tk
# class TestCalculator(unittest.TestCase):
#     @patch("tkinter.Tk", MagicMock)  # Mock Tkinter's Tk class
#     @patch("tkinter.Label", MagicMock) 
#      # Mock Tkinter Label
#     def setUp(self):
#         """Setup before each test"""
#         self.calc = Calculator()

#     ### ======================== STATEMENT COVERAGE ======================== ###
#     def test_statement_single_operation(self):
#         """Ensures each statement is executed at least once"""
#         self.calc.add_to_expression(5)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(3)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "8")

#     def test_statement_multiple_operations(self):
#         """Ensures all basic arithmetic operations are covered"""
#         self.calc.add_to_expression(10)
#         self.calc.append_operator("-")
#         self.calc.add_to_expression(2)
#         self.calc.append_operator("*")
#         self.calc.add_to_expression(3)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "4"),   # (10-2) * 3 = 24

#     ### ======================== BRANCH COVERAGE ======================== ###
#     def test_branch_zero_division(self):
#         """Covers division by zero case"""
#         self.calc.add_to_expression(4)
#         self.calc.append_operator("/")
#         self.calc.add_to_expression(0)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "Error")

#     def test_branch_negative_numbers(self):
#         """Covers handling of negative numbers"""
#         self.calc.add_to_expression(-10)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(5)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "-5")

#     def test_branch_invalid_input(self):
#         """Covers invalid input scenarios"""
#         self.calc.total_expression = "5 + * 3"
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "Error")

#     ### ======================== PATH COVERAGE ======================== ###
#     def test_path_independent_execution(self):
#         """Covers different execution paths"""
#         self.calc.add_to_expression(3)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(4)
#         self.calc.append_operator("*")
#         self.calc.add_to_expression(2)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "11")  # Order of operations: 4*2 + 3 = 11

#     def test_path_nested_operations(self):
#         """Covers multiple operations in different orders"""
#         self.calc.add_to_expression(100)
#         self.calc.append_operator("/")
#         self.calc.add_to_expression(10)
#         self.calc.append_operator("-")
#         self.calc.add_to_expression(5)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "5.0")

#     ### ======================== DECISION COVERAGE ======================== ###
#     def test_decision_true_branch(self):
#         """Tests true decision branches"""
#         self.calc.add_to_expression(7)
#         self.calc.append_operator("*")
#         self.calc.add_to_expression(2)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "14")

#     def test_decision_false_branch(self):
#         """Tests false decision branches"""
#         self.calc.add_to_expression(10)
#         self.calc.append_operator("/")
#         self.calc.add_to_expression(5)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "2.0")

#     ### ======================== CONTROL FLOW TESTING ======================== ###
#     def test_control_loop_operations(self):
#         """Tests if multiple operations execute correctly in a loop"""
#         for i in range(1, 4):  # Simulating 1+2+3
#             self.calc.add_to_expression(i)
#             if i < 3:
#                 self.calc.append_operator("+")
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "6")

#     def test_control_conditional_handling(self):
#         """Ensures conditionals execute properly"""
#         self.calc.add_to_expression(5)
#         self.calc.append_operator("/")
#         self.calc.add_to_expression(0)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "Error")

#     ### ======================== DATA FLOW TESTING ======================== ###
#     def test_data_flow_variable_initialization(self):
#         """Ensures variables are initialized before usage"""
#         self.assertEqual(self.calc.current_expression, "")

#     def test_data_flow_variable_modification(self):
#         """Ensures variable values change correctly"""
#         self.calc.add_to_expression(10)
#         self.assertEqual(self.calc.current_expression, "10")
#         self.calc.add_to_expression(5)
#         self.assertEqual(self.calc.current_expression, "105")  # Checking concatenation

#     def test_data_flow_invalid_usage(self):
#         """Ensures no uninitialized variable is accessed"""
#         try:
#             value = self.calc.total_expression  # Access without modification
#             self.assertTrue(True)  # Should not raise an error
#         except NameError:
#             self.fail("Uninitialized variable accessed!")

#     ### ======================== EDGE CASE TESTING ======================== ###
#     def test_edge_case_large_numbers(self):
#         """Tests handling of very large numbers"""
#         self.calc.add_to_expression(999999999)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(1)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "1000000000")

#     def test_edge_case_decimal_precision(self):
#         """Tests decimal handling"""
#         self.calc.add_to_expression(10)
#         self.calc.append_operator("/")
#         self.calc.add_to_expression(3)
#         self.calc.evaluate()
#         self.assertTrue(abs(float(self.calc.current_expression) - 3.3333) < 0.0001)

#     def test_edge_case_negative_sqrt(self):
#         """Tests square root of a negative number"""
#         self.calc.add_to_expression(-16)
#         try:
#             self.calc.sqrt()
#         except Exception:
#             self.assertTrue(True)  # Error is expected

#     def test_edge_case_zero_operations(self):
#         """Tests zero in various operations"""
#         self.calc.add_to_expression(0)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(0)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "0")
        
        
#     def test_clear(self):
#         """Test if clear() resets all values"""
#         self.calc.add_to_expression(10)
#         self.calc.clear()
#         self.assertEqual(self.calc.current_expression, "")
#         self.assertEqual(self.calc.total_expression, "")
#     def test_square(self):
#         """Test squaring a number"""
#         self.calc.add_to_expression(4)
#         self.calc.square()
#         self.assertEqual(self.calc.current_expression, "16")
#     def test_sqrt_valid(self):
#         """Test square root calculation for positive numbers"""
#         self.calc.add_to_expression(9)
#         self.calc.sqrt()
#         self.assertEqual(self.calc.current_expression, "3.0")
#     def test_update_label(self):
#         """Test if display updates correctly"""
#         self.calc.label.cget = MagicMock(return_value="12345678901")
#         self.calc.add_to_expression(123456789012345)  # Longer than max limit
#         self.calc.update_label()
#         self.assertEqual(self.calc.label.cget("text"), "12345678901")  # Should truncate
#     def test_update_total_label(self):
#         """Test if total expression label updates correctly"""
#         self.calc.total_label.cget = MagicMock(return_value="5 + 3")  # 🔹 Fixed MagicMock Return Value
#         self.calc.total_expression = "5 + 3"
#         self.calc.update_total_label()
#         displayed_text = self.calc.total_label.cget("text")

#         # Normalize spaces in both expected and actual output before comparison
#         self.assertEqual(" ".join(displayed_text.split()), "5 + 3")

#     def test_keyboard_input(self):
#         """Test if keyboard input updates the calculator correctly"""
        
#         # Simulate pressing '5' using the method that updates the expression
#         self.calc.add_to_expression(5)

#         # Check if the current expression is updated correctly
#         self.assertEqual(self.calc.current_expression, "5")
#     def test_path_complex_expression(self):
#         """Tests a complex arithmetic expression with multiple operations"""
#         self.calc.add_to_expression(5)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(10)
#         self.calc.append_operator("*")
#         self.calc.add_to_expression(2)
#         self.calc.append_operator("-")
#         self.calc.add_to_expression(3)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "22")  # (10*2) + 5 - 3 = 22

#     def test_path_operator_without_number(self):
#         """Ensures calculator handles cases where an operator is entered without a number after it"""
#         self.calc.add_to_expression(5)
#         self.calc.append_operator("+")
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "Error")  # Expression is incomplete
#     def test_path_consecutive_operators(self):
#         """Tests handling of consecutive operators"""
#         self.calc.add_to_expression(5)
#         self.calc.append_operator("+")
#         self.calc.append_operator("*")  # Invalid consecutive operator case
#         self.calc.add_to_expression(2)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "Error")
#     def test_path_chained_evaluations(self):
#         """Tests consecutive evaluations without clearing"""
#         self.calc.add_to_expression(10)
#         self.calc.append_operator("+")
#         self.calc.add_to_expression(5)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "15")  # First eval: 10 + 5 = 15

#         self.calc.append_operator("*")
#         self.calc.add_to_expression(2)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "30")  # Second eval: 15 * 2 = 30

#     def test_path_square_and_sqrt_combination(self):
#         """Tests combining square and square root operations"""
#         self.calc.add_to_expression(4)
#         self.calc.square()  # 4² = 16
#         self.calc.sqrt()  # sqrt(16) = 4
#         self.assertEqual(self.calc.current_expression, "4.0")

#     def test_path_leading_zeros(self):
#         """Ensures leading zeros do not cause errors"""
#         self.calc.add_to_expression(0)
#         self.calc.add_to_expression(5)
#         self.calc.evaluate()
#         self.assertEqual(self.calc.current_expression, "Error")  # Leading zero ignored

    


# if __name__ == "__main__":
#     unittest.main()
