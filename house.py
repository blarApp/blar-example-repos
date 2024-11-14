class House:
    def __init__(self, address, num_rooms, price):
        self.address = address
        self.num_rooms = num_rooms
        self.price = price

    def display_info(self):
        print("New house")
        print(f"Address: {self.address}")
        print(f"Number of rooms: {self.num_rooms}")
        print(f"Price: ${self.price}")


    def change_address(self, new):
        self.address = new
