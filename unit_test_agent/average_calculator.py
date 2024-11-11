# average_calculator.py

from math_operations import add, divide


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        print("no numbers encountered :(")
        raise ValueError("The list of numbers cannot be empty.")

    sum_of_numbers = 0
    for number in numbers:
        sum_of_numbers = add(sum_of_numbers, number)

    average = divide(sum_of_numbers, len(numbers))
    return average
