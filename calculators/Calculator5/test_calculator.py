
# import unittest
# from calculator_logic import binary_operation, unary_operation

# class TestCalculatorLogic(unittest.TestCase):

#     # ---------- Binary Operation Tests ----------

#     def test_addition(self):
#         self.assertEqual(binary_operation("5", "3", "+"), 8.0)

#     def test_subtraction(self):
#         self.assertEqual(binary_operation("10", "4", "-"), 6.0)

#     def test_multiplication(self):
#         self.assertEqual(binary_operation("6", "7", "*"), 42.0)

#     def test_division(self):
#         self.assertEqual(binary_operation("8", "2", "/"), 4.0)

#     def test_division_by_zero(self):
#         self.assertEqual(binary_operation("8", "0", "/"), "Error")

#     def test_modulus(self):
#         self.assertEqual(binary_operation("10", "3", "%"), 1.0)

#     def test_exponentiation(self):
#         self.assertEqual(binary_operation("2", "3", "^"), 8.0)

#     def test_invalid_binary_op(self):
#         self.assertEqual(binary_operation("4", "2", "&"), "Invalid")

#     def test_invalid_binary_input(self):
#         self.assertEqual(binary_operation("a", "2", "+"), "Error")
    
#     def test_addition_with_decimals(self):
#         self.assertEqual(binary_operation("5.5", "3.2", "+"), 8.7)

#     def test_subtraction_negative_result(self):
#         self.assertEqual(binary_operation("3", "10", "-"), -7.0)

#     def test_multiplication_with_zero(self):
#         self.assertEqual(binary_operation("5", "0", "*"), 0.0)

#     def test_division_with_decimals(self):
#         self.assertAlmostEqual(binary_operation("1", "3", "/"), 0.333, places=3)

#     def test_modulus_with_decimals(self):
#         self.assertEqual(binary_operation("5.5", "3", "%"), 2.5)

#     def test_exponentiation_fractional_exponent(self):
#         self.assertAlmostEqual(binary_operation("4", "0.5", "^"), 2.0, places=3)

#     def test_exponentiation_negative_base(self):
#         self.assertEqual(binary_operation("-2", "3", "^"), -8.0)

#     def test_exponentiation_zero_power(self):
#         self.assertEqual(binary_operation("5", "0", "^"), 1.0)

#     def test_empty_input_binary(self):
#         self.assertEqual(binary_operation("", "5", "+"), "Error")
#         self.assertEqual(binary_operation("5", "", "+"), "Error")
    
#     def test_division_by_negative(self):
#         self.assertEqual(binary_operation("10", "-2", "/"), -5.0)

#     def test_large_exponentiation(self):
#         self.assertEqual(binary_operation("2", "100", "^"), 1.2676506002282295e+30)

#     def test_zero_exponentiation(self):
#         self.assertEqual(binary_operation("0", "5", "^"), 0.0)

#     def test_large_numbers(self):
#         self.assertEqual(binary_operation("1000000000000", "5000000000000", "+"), 6000000000000.0)

#     def test_binary_with_non_numeric_strings(self):
#         self.assertEqual(binary_operation("abc", "123", "+"), "Error")

#     def test_division_negative_result(self):
#         self.assertEqual(binary_operation("-10", "2", "/"), -5.0)

#     def test_large_negative_numbers(self):
#         self.assertEqual(binary_operation("-1000000000000", "-5000000000000", "+"), -6000000000000.0)

#     def test_zero_base_negative_exponent(self):
#         self.assertEqual(binary_operation("0", "-5", "^"), "Error")  # Zero raised to negative power is undefined

#     def test_addition_with_string_input(self):
#         self.assertEqual(binary_operation("five", "3", "+"), "Error")

#     def test_large_decimal_addition(self):
#         self.assertEqual(binary_operation("123456.789", "987654.321", "+"), 1111111.11)

#     def test_exponentiation_float_base(self):
#         self.assertAlmostEqual(binary_operation("2.5", "3", "^"), 15.625, places=3)


#     # ---------- Unary Operation Tests ----------

#     def test_sin(self):
#         self.assertAlmostEqual(unary_operation("90", "sin"), 1.0, places=2)

#     def test_cos(self):
#         self.assertAlmostEqual(unary_operation("0", "cos"), 1.0, places=2)

#     def test_square_root(self):
#         self.assertEqual(unary_operation("16", "√"), 4.0)

#     def test_square(self):
#         self.assertEqual(unary_operation("4", "x²"), 16.0)

#     def test_cube(self):
#         self.assertEqual(unary_operation("2", "x³"), 8.0)

#     def test_factorial(self):
#         self.assertEqual(unary_operation("5", "!"), 120)

#     def test_log(self):
#         self.assertEqual(unary_operation("100", "log"), 2.0)

#     def test_inverse(self):
#         self.assertEqual(unary_operation("4", "1/x"), 0.25)

#     def test_inverse_zero(self):
#         self.assertEqual(unary_operation("0", "1/x"), "Error")

#     def test_factorial_float_input(self):
#         self.assertEqual(unary_operation("5.5", "!"), "Error")  # factorial expects int

#     def test_log_zero(self):
#         self.assertEqual(unary_operation("0", "log"), "Error")

#     def test_root_negative(self):
#         self.assertEqual(unary_operation("-4", "√"), "Error")

#     def test_unknown_unary_func(self):
#         self.assertEqual(unary_operation("5", "cot"), "Unknown")

#     def test_invalid_unary_input(self):
#         self.assertEqual(unary_operation("a", "sin"), "Error")

#     def test_sin_negative_angle(self):
#         self.assertAlmostEqual(unary_operation("-30", "sin"), -0.5, places=2)

#     def test_cos_negative_angle(self):
#         self.assertAlmostEqual(unary_operation("-60", "cos"), 0.5, places=2)

#     def test_square_root_decimal(self):
#         self.assertAlmostEqual(unary_operation("2", "√"), 1.41421, places=5)

#     def test_square_negative(self):
#         self.assertEqual(unary_operation("-3", "x²"), 9.0)

#     def test_cube_negative(self):
#         self.assertEqual(unary_operation("-2", "x³"), -8.0)

#     def test_factorial_zero(self):
#         self.assertEqual(unary_operation("0", "!"), 1)

#     def test_log_decimal(self):
#         self.assertAlmostEqual(unary_operation("10", "log"), 1.0, places=5)

#     def test_inverse_decimal(self):
#         self.assertEqual(unary_operation("0.5", "1/x"), 2.0)

#     def test_factorial_edge_case(self):
#         self.assertEqual(unary_operation("1", "!"), 1)

#     def test_log_one(self):
#         self.assertEqual(unary_operation("1", "log"), 0.0)

#     def test_log_negative(self):
#         self.assertEqual(unary_operation("-10", "log"), "Error")

#     def test_square_root_zero(self):
#         self.assertEqual(unary_operation("0", "√"), 0.0)

#     def test_factorial_negative_input(self):
#         self.assertEqual(unary_operation("-5", "!"), "Error")

#     def test_log_negative_input(self):
#         self.assertEqual(unary_operation("-1", "log"), "Error")

#     def test_factorial_of_decimal(self):
#         self.assertEqual(unary_operation("2.5", "!"), "Error")

#     def test_factorial_large_number(self):
#         self.assertEqual(unary_operation("171", "!"), "Too Large")

#     def test_invalid_unary_function(self):
#         self.assertEqual(unary_operation("2", "sec"), "Unknown")

#     def test_negative_input_log(self):
#         self.assertEqual(unary_operation("-10", "log"), "Error")

#     def test_large_input_log(self):
#         self.assertAlmostEqual(unary_operation("1000000", "log"), 6.0, places=1)

#     def test_square_root_large_number(self):
#         self.assertEqual(unary_operation("1000000", "√"), 1000.0)

#     def test_factorial_greater_than_170(self):
#         self.assertEqual(unary_operation("171", "!"), "Too Large")

#     def test_log_fraction(self):
#         self.assertAlmostEqual(unary_operation("0.5", "log"), -0.3010, places=4)

#     def test_factorial_non_integer(self):
#         self.assertEqual(unary_operation("5.1", "!"), "Error")

#     def test_log_between_zero_and_one(self):
#         self.assertAlmostEqual(unary_operation("0.1", "log"), -1.0, places=1)

#     def test_log_large_input(self):
#         self.assertAlmostEqual(unary_operation("1000000000", "log"), 9.0, places=1)

 

#     def test_factorial_large_float(self):
#         self.assertEqual(unary_operation("170.5", "!"), "Error")


#     # Edge cases

#     def test_empty_string_unary(self):
#         self.assertEqual(unary_operation("", "sin"), "Error")

#     def test_multiple_whitespaces_input(self):
#         self.assertEqual(binary_operation("  5  ", "  3  ", "+"), 8.0)
#         self.assertEqual(unary_operation("  16  ", "√"), 4.0)

#     def test_negative_exponentiation(self):
#         self.assertEqual(binary_operation("2", "-3", "^"), 0.125)

#     def test_empty_string_binary(self):
#         self.assertEqual(binary_operation("", "5", "+"), "Error")
#         self.assertEqual(binary_operation("5", "", "+"), "Error")

#     def test_multiple_operators(self):
#         self.assertEqual(binary_operation("5", "3", "+-"), "Invalid")  # Multiple operators at once

#     def test_multiple_whitespaces_unary(self):
#         self.assertEqual(unary_operation("   4   ", "√"), 2.0)  # Testing leading/trailing spaces

#     def test_inconsistent_number_format(self):
#         self.assertEqual(binary_operation("1,000", "500", "+"), "Error")  # Numbers with commas

#     def test_large_decimal_result(self):
#         self.assertEqual(binary_operation("123456.789", "987654.321", "+"), 1111111.11)
 
#     def test_negative_log_input(self):
#         self.assertEqual(unary_operation("-5", "log"), "Error")  # Logarithm of negative numbers is undefined

#     def test_factorial_of_zero(self):
#         self.assertEqual(unary_operation("0", "!"), 1)  # 0! is 1



#     def test_large_exponentiation_result(self):
#         self.assertEqual(binary_operation("999999", "100", "^"), "Error")  # Extremely large exponentiation


#     def test_unary_non_numeric_input(self):
#         self.assertEqual(unary_operation("abc", "sin"), "Error")


#     def test_factorial_max_input(self):
#         # Test the maximum value before factorial becomes too large
#         self.assertEqual(unary_operation("170", "!"), 'Too Large')

        



#     def test_whitespace_in_input(self):
#         self.assertEqual(binary_operation(" 5 ", " 3 ", "+"), 8.0)
#         self.assertEqual(unary_operation(" 16 ", "√"), 4.0)

#     def test_leading_zeros_input(self):
#         self.assertEqual(binary_operation("05", "03", "+"), 8.0)
#         self.assertEqual(unary_operation("016", "√"), 4.0)
    
#     def test_error_propagation_binary(self):
#     # Test that errors from first operand propagate
#         self.assertEqual(binary_operation("abc", "2", "+"), "Error")
#         # Test that errors from second operand propagate
#         self.assertEqual(binary_operation("2", "abc", "+"), "Error")
        
#     def test_error_propagation_unary(self):
#         # Test multiple error conditions
#         self.assertEqual(unary_operation("-1", "!"), "Error")
#         self.assertEqual(unary_operation("-1", "log"), "Error")
#         self.assertEqual(unary_operation("-1", "√"), "Error")
    
#     def test_factorial_overflow(self):
#         # Test edge case where factorial exceeds memory limits
#         self.assertEqual(unary_operation("10000", "!"), "Too Large")