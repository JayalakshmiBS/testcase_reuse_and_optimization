# import unittest
# from cal_logic import CalculatorLogic  # Make sure to save your code in calculator.py

# class TestCalculatorLogic(unittest.TestCase):

#     def setUp(self):
#         self.calc = CalculatorLogic()

#     # Statement & Basic Flow Coverage
#     def test_insert_basic(self):
#         self.calc.insert('1')
#         self.assertEqual(self.calc.expression, '1')

#     def test_insert_after_result(self):
#         self.calc.expression = "2+3"
#         self.calc.calculate()
#         self.calc.insert('4')
#         self.assertEqual(self.calc.expression, '4')

#     def test_insert_operator_after_result(self):
#         self.calc.expression = "2+3"
#         self.calc.calculate()
#         self.calc.insert('+')
#         self.assertEqual(self.calc.expression, '5+')

#     # Cancel (Clear all)
#     def test_cancel(self):
#         self.calc.insert('1')
#         self.calc.cancel()
#         self.assertEqual(self.calc.expression, '')

#     # Delete Last
#     def test_delete_last(self):
#         self.calc.insert('12')
#         self.calc.delete_last()
#         self.assertEqual(self.calc.expression, '1')

#     def test_delete_last_empty(self):
#         self.calc.delete_last()
#         self.assertEqual(self.calc.expression, '')

#     # Calculate valid
#     def test_calculate_valid_expression(self):
#         self.calc.insert('2+3')
#         result = self.calc.calculate()
#         self.assertEqual(result, '5')

#     # Calculate invalid syntax
#     def test_calculate_invalid_expression(self):
#         self.calc.insert('2++3')
#         result = self.calc.calculate()
#         self.assertEqual(result, '5')

#     # Division by zero
#     def test_division_by_zero(self):
#         self.calc.insert('1/0')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     # Edge cases
#     def test_empty_expression_calculate(self):
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_leading_zero(self):
#         self.calc.insert('0002+3')
#         result = self.calc.calculate()
#         self.assertEqual(result, '5')

#     def test_float_addition(self):
#         self.calc.insert('2.5+3.5')
#         result = self.calc.calculate()
#         self.assertEqual(result, '6.0')
    
#     def test_insert_leading_zero_after_operator(self):
#         self.calc.insert('3+0')
#         self.calc.insert('5')  # Should become '3+5' not '3+05'
#         self.assertEqual(self.calc.expression, '3+5')
    
#     def test_multiple_operators(self):
#         self.calc.insert('2+*3')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_expression_ends_with_operator(self):
#         self.calc.insert('3+')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')  # Or handle it based on how eval treats it

#     def test_unmatched_parentheses(self):
#         self.calc.insert('(2+3')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_consecutive_deletions(self):
#         self.calc.insert('123')
#         self.calc.delete_last()
#         self.calc.delete_last()
#         self.calc.delete_last()
#         self.assertEqual(self.calc.expression, '')

#     def test_only_decimal_point(self):
#         self.calc.insert('.')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_consecutive_decimal_points(self):
#         self.calc.insert('2..5')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_delete_after_result(self):
#         self.calc.insert('2+3')
#         self.calc.calculate()
#         self.calc.delete_last()
#         self.assertEqual(self.calc.expression, '')  # Because delete_last doesn't work after result

#     def test_operator_after_result(self):
#         self.calc.insert('4*5')
#         self.calc.calculate()
#         self.calc.insert('+')
#         self.calc.insert('6')
#         result = self.calc.calculate()
#         self.assertEqual(result, '26')

#     def test_insert_number_after_decimal_point(self):
#         self.calc.insert('.')
#         self.calc.insert('5')
#         self.assertEqual(self.calc.expression, '.5')

#     def test_insert_after_incomplete_expression(self):
#         self.calc.insert('2+')
#         self.calc.insert('3')
#         result = self.calc.calculate()
#         self.assertEqual(result, '5')

#     def test_delete_insert_cycle(self):
#         self.calc.insert('45')
#         self.calc.delete_last()
#         self.calc.insert('6')
#         result = self.calc.calculate()
#         self.assertEqual(result, '46')

#     def test_chaining_results(self):
#         self.calc.insert('10+5')
#         self.calc.calculate()  # Result: '15' (but expression resets)
        
#         # Start a new expression using the previous result manually
#         self.calc.insert('15*2')
#         result = self.calc.calculate()
#         self.assertEqual(result, '30')


#     def test_start_with_operator(self):
#         self.calc.insert('+3')
#         result = self.calc.calculate()
#         self.assertEqual(result, '3')  # Python allows unary +3

#     def test_double_decimal_error(self):
#         self.calc.insert('3.1.4')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_negative_number(self):
#         self.calc.insert('-4+6')
#         result = self.calc.calculate()
#         self.assertEqual(result, '2')

#     def test_calculate_then_delete_then_continue(self):
#         self.calc.insert('7+3')
#         self.calc.calculate()
#         self.calc.delete_last()  # should clear if logic prevents deletion after result
#         self.calc.insert('2')
#         result = self.calc.calculate()
#         self.assertEqual(result, '2')  # assumes delete clears entire expression after result


#     def test_empty_then_insert(self):
#         self.assertEqual(self.calc.expression, '')
#         self.calc.insert('9')
#         self.assertEqual(self.calc.expression, '9')

#     def test_insert_whitespace(self):
#         self.calc.insert('2 + 3')  # if insert supports raw string
#         result = self.calc.calculate()
#         self.assertEqual(result, '5')

#     def test_large_numbers(self):
#         self.calc.insert('1000000000+2000000000')
#         result = self.calc.calculate()
#         self.assertEqual(result, '3000000000')

#     def test_long_arithmetic_expression(self):
#         self.calc.insert('1+2+3+4+5+6+7+8+9+10')
#         result = self.calc.calculate()
#         self.assertEqual(result, '55')
    
#     def test_negative_in_parentheses(self):
#         self.calc.insert('-(2+3)')
#         result = self.calc.calculate()
#         self.assertEqual(result, '-5')

#     def test_nested_parentheses(self):
#         self.calc.insert('((2+3)*(4+5))')
#         result = self.calc.calculate()
#         self.assertEqual(result, '45')
    
#     def test_decimal_operations(self):
#         self.calc.insert('2.5+3.5')
#         result = self.calc.calculate()
#         self.assertEqual(result, '6.0')

#     def test_operator_precedence(self):
#         self.calc.insert('2+3*4')
#         result = self.calc.calculate()
#         self.assertEqual(result, '14')


#     def test_float_division(self):
#         self.calc.insert('5.0/2.0')
#         result = self.calc.calculate()
#         self.assertEqual(result, '2.5')

#     def test_multiple_decimal_points_in_number(self):
#         self.calc.insert('3.14.15')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_empty_parentheses(self):
#         self.calc.insert('()')
#         result = self.calc.calculate()
#         self.assertEqual(result, '()')

#     def test_invalid_input(self):
#         self.calc.insert('2+3a')
#         result = self.calc.calculate()
#         self.assertEqual(result, 'Error')

#     def test_large_number_of_digits(self):
#         self.calc.insert('99999999999+1')
#         result = self.calc.calculate()
#         self.assertEqual(result, '100000000000')

#     def test_unary_minus_middle(self):
#         self.calc.insert('5*-2')
#         result = self.calc.calculate()
#         self.assertEqual(result, '-10')
    
#     def test_nested_with_precedence(self):
#         self.calc.insert('((1+2)*3+4)/2')
#         result = self.calc.calculate()
#         self.assertEqual(result, '6.5')

#     def test_insert_after_multiple_cancels(self):
#         self.calc.insert('123')
#         self.calc.cancel()
#         self.calc.insert('4')
#         result = self.calc.calculate()
#         self.assertEqual(result, '4')











    



# '''

# def suite_edge_coverage():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_empty_expression_calculate'))  # Empty expression
#     suite.addTest(TestCalculatorLogic('test_leading_zero'))               # Leading zero handling
#     suite.addTest(TestCalculatorLogic('test_only_decimal_point'))         # Only decimal point input
#     suite.addTest(TestCalculatorLogic('test_consecutive_decimal_points')) # Invalid multiple decimal points
#     suite.addTest(TestCalculatorLogic('test_double_decimal_error'))       # Multiple decimal points in number
#     return suite

# def suite_branch_coverage():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_calculate_invalid_expression'))  # Invalid syntax (like '2++3')
#     suite.addTest(TestCalculatorLogic('test_division_by_zero'))              # Division by zero
#     suite.addTest(TestCalculatorLogic('test_multiple_operators'))            # Invalid operator handling
#     suite.addTest(TestCalculatorLogic('test_expression_ends_with_operator')) # Expression ends with operator
#     suite.addTest(TestCalculatorLogic('test_unmatched_parentheses'))         # Unmatched parentheses
#     return suite

# def suite_decision_coverage():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_calculate_valid_expression'))  # Valid expression
#     suite.addTest(TestCalculatorLogic('test_calculate_invalid_expression'))  # Invalid expression
#     suite.addTest(TestCalculatorLogic('test_calculate_then_delete_then_continue'))  # Deletion after calculation
#     return suite

# def suite_path_coverage():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_insert_after_result'))  # Insert after result
#     suite.addTest(TestCalculatorLogic('test_cancel'))               # Canceling operation
#     suite.addTest(TestCalculatorLogic('test_delete_last'))         # Deleting last input
#     suite.addTest(TestCalculatorLogic('test_chaining_results'))    # Chaining multiple operations
#     return suite

# def suite_data_flow_coverage():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_insert_number_after_decimal_point')) # Inserting number after decimal
#     suite.addTest(TestCalculatorLogic('test_insert_after_incomplete_expression'))  # Insert number after incomplete expression
#     suite.addTest(TestCalculatorLogic('test_insert_leading_zero_after_operator'))  # Zero handling after operator
#     return suite

# def suite_control_flow_coverage():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_calculate_valid_expression'))  # Valid expression calculation
#     suite.addTest(TestCalculatorLogic('test_delete_last_empty'))          # Deleting when empty
#     suite.addTest(TestCalculatorLogic('test_consecutive_deletions'))     # Multiple deletions
#     suite.addTest(TestCalculatorLogic('test_delete_after_result'))       # Deleting after result
#     return suite







# def suite_basic_operations():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_insert_basic'))
#     suite.addTest(TestCalculatorLogic('test_insert_after_result'))
#     suite.addTest(TestCalculatorLogic('test_insert_operator_after_result'))
#     suite.addTest(TestCalculatorLogic('test_calculate_valid_expression'))
#     suite.addTest(TestCalculatorLogic('test_float_addition'))
#     return suite

# def suite_error_handling():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_calculate_invalid_expression'))
#     suite.addTest(TestCalculatorLogic('test_division_by_zero'))
#     suite.addTest(TestCalculatorLogic('test_multiple_operators'))
#     suite.addTest(TestCalculatorLogic('test_expression_ends_with_operator'))
#     suite.addTest(TestCalculatorLogic('test_unmatched_parentheses'))
#     suite.addTest(TestCalculatorLogic('test_only_decimal_point'))
#     suite.addTest(TestCalculatorLogic('test_consecutive_decimal_points'))
#     suite.addTest(TestCalculatorLogic('test_double_decimal_error'))
#     return suite

# def suite_edge_cases():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_leading_zero'))
#     suite.addTest(TestCalculatorLogic('test_insert_leading_zero_after_operator'))
#     suite.addTest(TestCalculatorLogic('test_start_with_operator'))
#     suite.addTest(TestCalculatorLogic('test_negative_number'))
#     return suite

# def suite_deletion_and_chaining():
#     suite = unittest.TestSuite()
#     suite.addTest(TestCalculatorLogic('test_delete_last'))
#     suite.addTest(TestCalculatorLogic('test_delete_last_empty'))
#     suite.addTest(TestCalculatorLogic('test_consecutive_deletions'))
#     suite.addTest(TestCalculatorLogic('test_delete_after_result'))
#     suite.addTest(TestCalculatorLogic('test_calculate_then_delete_then_continue'))
#     suite.addTest(TestCalculatorLogic('test_chaining_results'))
#     suite.addTest(TestCalculatorLogic('test_delete_insert_cycle'))
#     return suite

# def suite_all():
#     return unittest.TestLoader().loadTestsFromTestCase(TestCalculatorLogic)

# '''
# if __name__ == '__main__':
#     #print("Running all tests...\n")
#     '''
#     runner = unittest.TextTestRunner(verbosity=2)
#     # To run a specific suite, replace `suite_all()` with the desired one
#     runner.run(suite_all())
#     runner.run(suite_edge_coverage())  # To test edge coverage
#     runner.run(suite_branch_coverage())  # To test branch coverage
#     runner.run(suite_decision_coverage())  # To test decision coverage
#     runner.run(suite_path_coverage())  # To test path coverage
#     runner.run(suite_data_flow_coverage())  # To test data flow coverage
#     runner.run(suite_control_flow_coverage())  # To test control flow coverage
#     '''

#     unittest.main()
