from tkinter import *
import re
# Logic class (independent from GUI)
class CalculatorLogic:
    def __init__(self):
        self.expression = ""

    def click_button(self, value):
        self.expression += str(value)
        return self.expression

    def clear(self):
        self.expression = ""
        return self.expression
    def preprocess_expression(self, expr):
            # Replace numbers with stripped leading zeros
            return re.sub(r'\b0+(\d+)', r'\1', expr)

    def delete(self):
        self.expression = self.expression[:-1]
        return self.expression

    def evaluate(self):
        try:
            # Validate only allowed characters
            if not re.fullmatch(r"[0-9+\-*/(). ]*", self.expression):
                raise ValueError("Invalid characters")

            # Sanitize expression to remove leading zeros
            cleaned_expr = self.preprocess_expression(self.expression)

            result = str(eval(cleaned_expr))
            self.expression = result
            return result
        except Exception:
            self.expression = ""
            return "Error"


