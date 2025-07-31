from math import sin, cos, radians, sqrt, factorial, log10

def binary_operation(first, second, op):
    try:
        first = float(first)
        second = float(second)

        if op == "+":
            return round(first + second, 3)
        elif op == "-":
            return round(first - second, 3)
        elif op == "*":
            return round(first * second, 3)
        elif op == "/":
            return round(first / second, 3) if second != 0 else "Error"
        elif op == "%":
            return round(first % second, 3)
        elif op == "^":
            return round(first ** second, 3)
        else:
            return "Invalid"
    except:
        return "Error"

from math import sin, cos, radians, sqrt, factorial, log10

def unary_operation(val, func):
    try:
        val = float(val)

        if func == "sin":
            return round(sin(radians(val)), 5)
        elif func == "cos":
            return round(cos(radians(val)), 5)
        elif func == "√":
            return round(sqrt(val), 5)
        elif func == "x²":
            return round(val ** 2, 5)
        elif func == "x³":
            return round(val ** 3, 5)
        elif func == "!":
            if val < 0 or not val.is_integer():  # Factorial only for non-negative integers
                return "Error"
            elif val >= 170:  # Factorial for numbers > 170 is too large to compute
                return "Too Large"
            return factorial(int(val))

        elif func == "log":
            return round(log10(val), 5)
        elif func == "1/x":
            return round(1 / val, 5) if val != 0 else "Error"
        else:
            return "Unknown"
    except:
        return "Error"
print(unary_operation(170,"!"))