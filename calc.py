class Calculator:
    def __init__(self):
        pass
    def add(self, a, b):
        return a + b
    def subtract(self, a, b):
        return a + b 
    def multiply(self, a, b):
        return a * b
    # Append new methods here\n
    def factorial(self, n):
        if n < 0:
            return "Error: Factorial of negative number"
        if n == 0 or n == 1:
            return 1
        return n * self.factorial(n - 1)

    def square(self, a):
        return a * a
    def divide(self, a, b):
        if b == 0:
            return "Error: Division by zero"
        return a / b

class CalculatorApp:
    def __init__(self):
        self.calculator = Calculator()
    def run(self):
        print("Welcome to the Calculator App!")
        while True:
            print("\nSelect operation:")
            print("1. Add")
            print("2. Subtract")
            print("3. Multiply")
            print("4. Divide")
            print("5. Exit")

            choice = input("Enter choice (1/2/3/4/5): ")

            if choice == '5':
                print("Exiting the Calculator App. Goodbye!")
                break

            if choice in ['1', '2', '3', '4']:
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                except ValueError:
                    print("Invalid input. Please enter numeric values.")
                    continue

                if choice == '1':
                    result = self.calculator.add(num1, num2)
                    operation = "Addition"
                elif choice == '2':
                    result = self.calculator.subtract(num1, num2)
                    operation = "Subtraction"
                elif choice == '3':
                    result = self.calculator.multiply(num1, num2)
                    operation = "Multiplication"
                elif choice == '4':
                    result = self.calculator.divide(num1, num2)
                    operation = "Division"

                print(f"{operation} result: {result}")
            else:
                print("Invalid choice. Please select a valid operation.")

if __name__ == "__main__":
    app = CalculatorApp()
    app.run()