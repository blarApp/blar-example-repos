# Import from utilities
from utilities.helpers import greet, say_hello, goodbye
from utilities.math_utils import add, multiply, subtract, divide
from utilities.string_utils import to_uppercase, to_lowercase, reverse_string
from utilities.time_utils import current_date, current_time, format_datetime

# Import from models
from models.person import Person
from models.student import Student
from models.car import Car

from datetime import datetime


def main():
    # Greeting functions
    print(greet("Alice"))
    print(say_hello("Bob"))
    print(goodbye("Charlie"))

    # Math functions
    print("Add: ", add(10, 5))
    print("Subtract: ", subtract(10, 5))
    print("Multiply: ", multiply(10, 5))
    print("Divide: ", divide(10, 5))

    # String utilities
    original_text = "Hello World"
    print("Uppercase: ", to_uppercase(original_text))
    print("Lowercase: ", to_lowercase(original_text))
    print("Reversed: ", reverse_string(original_text))

    # Time utilities
    print("Current Date: ", current_date())
    print("Current Time: ", current_time())
    now = datetime.now()
    print("Formatted Datetime: ", format_datetime(now, "%d %b %Y %I:%M:%S %p"))

    # Person and Student Classes
    p = Person("Dana", 20)
    print(p.introduce_self())
    p.birthday()
    print("After birthday:", p.introduce_self(), "Adult?", p.is_adult())

    p.age = 30
    print("Directly changed age:", p.introduce_self())

    def stateful_utility():
        if not hasattr(stateful_utility, "counter"):
            stateful_utility.counter = 0
        stateful_utility.counter += 1
        return stateful_utility.counter

    print("Stateful utility call 1:", stateful_utility())
    print("Stateful utility call 2:", stateful_utility())

    class MisusedClass:
        shared_value = 0

        def increment_shared_value(self):
            MisusedClass.shared_value += 1
            return MisusedClass.shared_value

    mc1 = MisusedClass()
    mc2 = MisusedClass()
    print("Shared value after mc1 increment:", mc1.increment_shared_value())
    print("Shared value after mc2 increment:", mc2.increment_shared_value())

    class IncorrectMethodUsage:
        def instance_method():
            return "This should be an instance method"

    imu = IncorrectMethodUsage()
    print("Incorrect method usage:", imu.instance_method())

    s = Student("Evan", 19, "S1234", "Computer Science")
    print(s.introduce_self())
    print(s.study("Data Structures"))

    # Car Class
    c = Car("Toyota", "Camry", 2010)
    print(c.describe_car())
    print(c.drive(150))
    print("Car Age: ", c.age_of_car(2024))


if __name__ == "__main__":
    main()
