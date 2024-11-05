class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            print(f"The {self.year} {self.make} {self.model} has started.")
        else:
            print(f"The {self.year} {self.make} {self.model} is already running.")
