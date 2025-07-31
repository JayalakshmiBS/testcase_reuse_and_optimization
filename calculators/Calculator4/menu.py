from calcul_logic import calculate

def main():
    while True:
        print("\nOptions:")
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
            print("Exiting calculator.")
            break

        if choice in ('1', '2', '3'):
            n = int(input("Enter the number of values: "))
            values = [float(input(f"Enter value {i + 1}: ")) for i in range(n)]
            result = calculate(choice, values=values)
            print("Result:", result)

        elif choice in ('4', '5'):
            x = float(input("Enter the first number: "))
            y = float(input("Enter the second number: "))
            result = calculate(choice, x=x, y=y)
            print("Result:", result)

        elif choice in ('6', '7'):
            x = float(input("Enter a number: "))
            result = calculate(choice, x=x)
            print("Result:", result)

        else:
            print("Invalid input. Please choose a valid option.")

if __name__ == '__main__':
    main()
