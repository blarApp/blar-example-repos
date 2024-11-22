# main.py

from utils import greet_user, add_numbers
import config

def main():
    """
    Main function to demonstrate the script's functionality.
    """
    # Greet the user with a default name from config
    print(greet_user(config.DEFAULT_USER_NAME))
    
    # Prompt user for numbers and perform addition
    try:
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        result = add_numbers(num1, num2)
        print(f"The result of adding {num1} and {num2} is: {result}")
    except ValueError:
        print("Please enter valid numbers.")

if __name__ == "__main__":
    main()
