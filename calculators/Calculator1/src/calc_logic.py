import math

class CalculatorLogic:
    def __init__(self):
        self.total_expression = ""
        self.current_expression = ""

    def add_to_expression(self, value):
        self.current_expression += str(value)

    def append_operator(self, operator):
        self.total_expression += self.current_expression + operator
        self.current_expression = ""

    def clear(self):
        self.total_expression = ""
        self.current_expression = ""

    def square(self):
        try:
            self.current_expression = str(eval(f"{self.current_expression}**2"))
        except Exception:
            self.current_expression = "Error"

    def sqrt(self):
        try:
            num = float(self.current_expression)
            if num < 0:
                self.current_expression = "Error"
            else:
                self.current_expression = str(math.sqrt(num))
        except Exception:
            self.current_expression = "Error"

    def evaluate(self):
        self.total_expression += self.current_expression
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception:
            self.current_expression = "Error"

    def get_current_expression(self):
        return self.current_expression[:11]

    def get_total_expression(self):
        return self.total_expression
