def add(a: float, b: float) -> float:
    """Add two numbers and return the result."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the result."""
    return a * b

def subtract(a: float, b: float) -> float:
    """Subtract b from a."""
    return a - b

def divide(a: float, b: float) -> float:
    """Divide a by b, handling division by zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
