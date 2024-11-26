class Car:
    def __init__(self, make, model, fuel_level=100):
        self.make = make
        self.model = model
        self.fuel_level = fuel_level

    def drive(self, distance):
        fuel_needed = distance * 0.1  # Simple fuel consumption
        if self.fuel_level >= fuel_needed:
            self.fuel_level -= fuel_needed
            print(f"Drove {distance} km. Fuel level: {self.fuel_level}%.")
        else:
            print("Not enough fuel to drive.")

    def refuel(self, amount):
        self.fuel_level = min(self.fuel_level + amount, 100)
        print(f"Refueled. Fuel level: {self.fuel_level}%.")


    def display(self):
        return



# Example usage
car = Car("Honda", "Civic")
car.drive(50)
car.refuel(20)
