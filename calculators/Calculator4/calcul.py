import math

# Function to add n numbers
def add(numbers):
    return sum(numbers)

# Function to subtract n numbers
def subtract(numbers):
    result = numbers[0]
    for num in numbers[1:]:
        result -= num
    return result

# Function to multiply n numbers
def multiply(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

# Function to perform division
def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

# Function to perform modulus
def modulus(x, y):
    if y == 0:
        return "Cannot perform modulus by zero"
    return x % y

# Function to calculate sine
def sine(x):
    return math.sin(math.radians(x))

# Function to calculate cosine
def cosine(x):
    return math.cos(math.radians(x))

# Main calculator loop
while True:
    print("Options:")
    print("1 - Addition of n numbers")
    print("2 - Subtraction of n numbers")
    print("3 - Multiplication of n numbers")
    print("4 - Division")
    print("5 - Modulus")
    print("6 - Sine")
    print("7 - Cosine")
    print("0 - Quit")

    choice = input("Enter your choice: ")

    if choice == '0':
        break

    if choice in ('1', '2', '3', '6', '7'):
        if choice in ('6', '7'):
            num = float(input("Enter a number: "))
            if choice == '6':
                print("Result:", sine(num))
            else:
                print("Result:", cosine(num))
        else:
            n = int(input("Enter the number of values: "))
            values = [float(input(f"Enter value {i + 1}: ")) for i in range(n)]
            if choice == '1':
                print("Result:", add(values))
            elif choice == '2':
                print("Result:", subtract(values))
            elif choice == '3':
                print("Result:", multiply(values))
    elif choice in ('4', '5'):
        x = float(input("Enter the first number: "))
        y = float(input("Enter the second number: "))
        if choice == '4':
            print("Result:", divide(x, y))
        else:
            print("Result:", modulus(x, y))
    else:
        print("Invalid input. Please choose a valid option.")