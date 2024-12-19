class Person:
    def __init__(self, name, age):

        self.name_lastname = name
        self.age = age

    def greet(self):
        print(f"Hello, my name is {self.name} and I am {self.age} years old.")

    def run(self):
        print(f"{self.name} is running a lot"
