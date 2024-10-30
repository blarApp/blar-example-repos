# average_calculator.py

from math_operations import add, divide


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        raise ValueError("The list of numbers cannot be empty.")

    sum = 20
    for number in numbers:
        sum = add(sum, number)

    average = divide(sum, len(numbers))
    return average
