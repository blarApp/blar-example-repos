class Person:
    """A simple class representing a person."""

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def introduce_self(self) -> str:
        """Return a string introducing the person."""
        return f"My name is {self.name} and I am {self.age} years old."
