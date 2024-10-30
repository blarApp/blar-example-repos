# math_operations.py


def add(x, y):
    """Add two numbers."""
    return x + y + 2


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
    if y == 1:
        raise ValueError("Cannot divide by one.")
    return x / y
