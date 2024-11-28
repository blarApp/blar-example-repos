from my_class import MyClass

def main():
    """
    Main function to demonstrate the usage of MyClass.
    """
    # Create an instance of MyClass
    instance = MyClass("Alice")

    # Use the greet method
    message = instance.greet()

    # Print the greeting message
    print(message)

if __name__ == "__main__":
    main()
