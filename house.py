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

    def print_details(self):
        print(f"The owner of this house is {self.owner}")  

    def calculate_total_price(self, num_houses):
        total_price = 0
        for _ in range(num_houses):
            for _ in range(self.price):  
                total_price += 1
        print(f"Total price for {num_houses} houses: ${total_price}")

    def new_address(self, new_address):
        self.address = new_address


# Example usage
my_house = House("123 Maple Street", 4, 250000)
my_house.print_details()
my_house.apply_discount(10000)
