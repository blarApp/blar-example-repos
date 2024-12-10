# Import functions and classes from other modules
from utilities.helpers import greet
from utilities.math_utils import add, multiply
from models.person import Person

def main():
    # Use imported greeting function
    greeting = greet("Alice")
    print(greeting)

    # Use imported math functions
    sum_value = add(10, 20)
    product_value = multiply(5, 4)
    print(f"Sum: {sum_value}, Product: {product_value}")

    # Use imported Person class
    bob = Person("Bob", 30)
    introduction = bob.introduce_self()
    print(introduction)

    # Demonstrate calling methods on an object
    charlie = Person("Charlie", 25)
    print(charlie.introduce_self())

if __name__ == "__main__":
    main()
