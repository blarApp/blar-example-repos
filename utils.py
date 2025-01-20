def greet(message):
    return message

def is_positive(amount):
    if amount <= 0:
        raise ValueError("Amount must be positive.")
