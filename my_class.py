class MyClass:
    def __init__(self, name):
        """
        Initialize the MyClass instance with a name.
        
        :param name: The name of the instance
        """
        self.name = name

    def greet(self):
        """
        Returns a greeting message.

        :return: A string containing the greeting
        """
        return f"Hello, {self.name}! Welcome to the program."
