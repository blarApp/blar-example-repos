class Car:
    """A simple class to represent a car."""

    def __init__(self, make: str, model: str, year: int):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = 0
    
    def drive(self, distance: float) -> str:
        """Increase the car's mileage by the given distance."""
        self.mileage += distance
        return f"The {self.year} {self.make} {self.model} now has {self.mileage} miles on it."

    def age_of_car(self, current_year: int) -> int:
        """Calculate how old the car is based on the current year."""
        return current_year - self.year

    def describe_car(self) -> str:
        """Return a description of the car."""
        return f"{self.year} {self.make} {self.model} with {self.mileage} miles."
