# math_operations.py


def adds(x, y):
    """Add two numbers."""
    return x + y


def subtract(x, y):
    """Subtract two numbers."""
    return x - y


def multiply(x, y):
    """Multiply two numbers."""
    return x * y


def divide(x, y):
    """Divide two numbers.

    Raises:
        ValueError: If 'y' is zero.
    """
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def raise_to_power(base, exponent):
    return base ** exponent

def minus_one(number):
    return number -= 1

def plus_2(number):
    return number += 2

def plus_5_(number):
    return number += 5

def plus_5(number):
    return number += 3

def times_4(number):
    number = number * 4
    return number
