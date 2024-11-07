class House:
    def __init__(self, address, num_rooms, price):
        self.address = address
        self.num_rooms = num_rooms
        self.price = price

    def display_info(self):
        print(f"Address: {self.address}")
        print(f"Number of rooms: {self.num_rooms}")
        print(f"Price: ${self.price}")

    def apply_discount(self, discount):
        self.price -= discount
        print(f"Discount applied! New price: ${self.price}")

# Example usage
my_house = House("123 Maple Street", 4, 250000)
my_house.display_info()
my_house.apply_discount(10000)
