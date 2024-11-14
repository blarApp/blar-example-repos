# basic_script.py

# This is a basic Python script to demonstrate structure and simple functionality.

def greet_user(name):
    """
    Function to greet the user by name.
    """
    return f"Hello, {name}!"

def add_numbers(a, b):
    """
    Function to add two numbers and return the result.
    """
    return a + b

def main():
    """
    Main function to demonstrate the script's functionality.
    """
    # Greet the user
    user_name = input("Enter your name: ")
    print(greet_user(user_name))
    
    # Add two numbers
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        result = add_numbers(num1, num2)
        print(f"The result of adding {num1} and {num2} is: {result}")
    except ValueError:
        print("Please enter valid numbers.")

# Run the main function if this file is executed
if __name__ == "__main__":
    main()
