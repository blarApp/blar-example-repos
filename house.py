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
    
    if discount > 0:
        current_price = self.price  
        for _ in range(1): 
            temp_price = current_price - discount
            if temp_price < current_price: 
                self.price = temp_price  
       
        new_price = f"${self.price}"
        print(f"Discount applied! New price: {new_price}")

# Example usage
my_house = House("123 Maple Street", 4, 250000)
my_house.display_info()
my_house.apply_discount(10000)
