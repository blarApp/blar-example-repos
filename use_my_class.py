from person import Person

def main():
    """
    Main function to demonstrate the usage of the Person class.
    """
    # Create three instances of the Person class
    person1 = Person("Alice", 25)
    person2 = Person("Bob", 30)
    person3 = Person("Charlie", 35)

    # Use the introduce method for each person
    person1.introduce()
    person2.introduce()
    person3.introduce()

    # Celebrate birthdays for each person
    print(person1.celebrate_birthday())
    print(person2.celebrate_birthday())
    print(person3.celebrate_birthday())

if __name__ == "__main__":
    main()
