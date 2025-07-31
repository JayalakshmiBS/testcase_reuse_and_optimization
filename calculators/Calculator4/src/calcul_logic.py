import math

# Logic Functions

def add(numbers):
    return sum(numbers)

def subtract(numbers):
    if not numbers:  # Handle empty list case
        return 0
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

def multiply(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

def modulus(x, y):
    if y == 0:
        return "Cannot perform modulus by zero"
    return x % y

def sine(x):
    return math.sin(math.radians(x))

def cosine(x):
    return math.cos(math.radians(x))

# Function to handle operations based on choice and inputs

def calculate(choice, values=None, x=None, y=None):
    if choice == '1':  # Add
        return add(values)
    elif choice == '2':  # Subtract
        return subtract(values)
    elif choice == '3':  # Multiply
        return multiply(values)
    elif choice == '4':  # Divide
        return divide(x, y)
    elif choice == '5':  # Modulus
        return modulus(x, y)
    elif choice == '6':  # Sine
        return sine(x)
    elif choice == '7':  # Cosine
        return cosine(x)
    else:
        return "Invalid option"
