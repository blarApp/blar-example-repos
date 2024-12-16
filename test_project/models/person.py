class Person:
    """A simple class representing a person."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def introduce_self(self) -> str:
        """Return a string introducing the person."""
        return f"My name is {self.name} and I am {self.age} years old."

    def birthday(self):
        """Increment the person's age by one year."""
        self.age += 1

    def is_adult(self) -> bool:
        """Determine if the person is an adult."""
        return self.age >= 18
