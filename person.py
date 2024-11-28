class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")
        return 
        
    def celebrate_birthday(self):
        self.age += 1
        return f"Happy Birthday, {self.name}! You are now {self.age} years old."
